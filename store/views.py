from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.db import transaction
from django.db.models import Avg, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme

from .cart import FREE_SHIPPING_THRESHOLD, STANDARD_SHIPPING, cart_items
from .forms import (
    CheckoutForm,
    CustomerProfileForm,
    ReviewForm,
    SignUpForm,
    UserProfileForm,
)
from .models import Category, CustomerProfile, Order, OrderItem, Product, Review


def home(request):
    products = Product.objects.filter(available=True, stock__gt=0).select_related('category')
    return render(request, 'store/home.html', {
        'categories': Category.objects.all(),
        'featured_products': products.filter(featured=True)[:8],
        'new_products': products.order_by('-created_at')[:8],
    })


def products(request):
    product_list = Product.objects.filter(available=True).select_related('category').annotate(
        rating_average=Avg('reviews__rating'),
    )
    query = request.GET.get('q', '').strip()
    category_slug = request.GET.get('category', '').strip()
    sort = request.GET.get('sort', 'featured')
    if query:
        product_list = product_list.filter(Q(name__icontains=query) | Q(description__icontains=query) | Q(category__name__icontains=query))
    if category_slug:
        product_list = product_list.filter(category__slug=category_slug)
    sort_options = {'price_low': 'price', 'price_high': '-price', 'newest': '-created_at', 'featured': '-featured'}
    product_list = product_list.order_by(sort_options.get(sort, '-featured'), '-created_at')
    return render(request, 'store/products.html', {
        'products': product_list,
        'categories': Category.objects.all(),
        'query': query,
        'active_category': category_slug,
        'sort': sort,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product.objects.select_related('category'), slug=slug, available=True)
    review_form = ReviewForm()
    return render(request, 'store/product_detail.html', {
        'product': product,
        'reviews': product.reviews.select_related('user').all(),
        'review_form': review_form,
    })


@login_required
def add_review(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            Review.objects.update_or_create(
                product=product,
                user=request.user,
                defaults=form.cleaned_data,
            )
            messages.success(request, 'Your review has been saved.')
        else:
            messages.error(request, 'Please check the review details and try again.')
    return redirect('store:product_detail', slug=slug)


def add_to_cart(request, product_id):
    if request.method != 'POST':
        return redirect('store:products')
    product = get_object_or_404(Product, pk=product_id, available=True)
    cart = request.session.get('cart', {})
    key = str(product.pk)
    try:
        requested = max(1, int(request.POST.get('quantity', 1)))
    except (TypeError, ValueError):
        requested = 1
    current = int(cart.get(key, 0))
    if product.stock < 1:
        messages.error(request, 'This item is currently out of stock.')
    else:
        cart[key] = min(current + requested, product.stock)
        request.session['cart'] = cart
        messages.success(request, f'{product.name} added to your cart.')
    redirect_to = request.POST.get('next', '')
    if not url_has_allowed_host_and_scheme(redirect_to, allowed_hosts={request.get_host()}):
        redirect_to = 'store:cart'
    return redirect(redirect_to)


def cart(request):
    items = cart_items(request)
    subtotal = sum((item['line_total'] for item in items), Decimal('0.00'))
    shipping = Decimal('0.00') if subtotal >= FREE_SHIPPING_THRESHOLD or not subtotal else STANDARD_SHIPPING
    return render(request, 'store/cart.html', {
        'items': items,
        'subtotal': subtotal,
        'shipping': shipping,
        'total': subtotal + shipping,
        'free_shipping_threshold': FREE_SHIPPING_THRESHOLD,
    })


def update_cart(request):
    if request.method == 'POST':
        cart_data = request.session.get('cart', {})
        for key in list(cart_data):
            try:
                quantity = int(request.POST.get(f'quantity_{key}', cart_data[key]))
            except (TypeError, ValueError):
                quantity = 1
            product = Product.objects.filter(pk=key, available=True).first()
            if product is None or quantity < 1:
                cart_data.pop(key, None)
            else:
                cart_data[key] = min(quantity, product.stock)
                if not cart_data[key]:
                    cart_data.pop(key, None)
        request.session['cart'] = cart_data
        messages.success(request, 'Your cart has been updated.')
    return redirect('store:cart')


def remove_from_cart(request, product_id):
    if request.method == 'POST':
        cart_data = request.session.get('cart', {})
        cart_data.pop(str(product_id), None)
        request.session['cart'] = cart_data
        messages.success(request, 'Item removed from your cart.')
    return redirect('store:cart')


@login_required
def checkout(request):
    items = cart_items(request)
    if not items:
        messages.info(request, 'Your cart is empty.')
        return redirect('store:products')
    profile, _ = CustomerProfile.objects.get_or_create(user=request.user)
    initial = {field: getattr(profile, field) for field in ('address', 'city', 'postal_code', 'phone')}
    subtotal = sum((item['line_total'] for item in items), Decimal('0.00'))
    shipping = Decimal('0.00') if subtotal >= FREE_SHIPPING_THRESHOLD else STANDARD_SHIPPING
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    checked_items = []
                    for item in items:
                        product = Product.objects.select_for_update().get(pk=item['product'].pk)
                        if not product.available or product.stock < item['quantity']:
                            raise ValueError(f'{product.name} no longer has enough stock.')
                        checked_items.append((product, item['quantity']))
                    order = Order.objects.create(
                        user=request.user,
                        address=form.cleaned_data['address'],
                        city=form.cleaned_data['city'],
                        postal_code=form.cleaned_data['postal_code'],
                        phone=form.cleaned_data['phone'],
                        notes=form.cleaned_data['notes'],
                        subtotal=subtotal,
                        shipping=shipping,
                        total=subtotal + shipping,
                    )
                    for product, quantity in checked_items:
                        OrderItem.objects.create(
                            order=order,
                            product=product,
                            product_name=product.name,
                            unit_price=product.price,
                            quantity=quantity,
                        )
                        product.stock -= quantity
                        product.save(update_fields=['stock'])
                    profile.phone = form.cleaned_data['phone']
                    profile.address = form.cleaned_data['address']
                    profile.city = form.cleaned_data['city']
                    profile.postal_code = form.cleaned_data['postal_code']
                    profile.save()
            except (Product.DoesNotExist, ValueError) as error:
                form.add_error(None, str(error) or 'A product in your cart is no longer available.')
            else:
                request.session['cart'] = {}
                messages.success(request, 'Order placed. Thank you for shopping with Pexo Market!')
                return redirect('store:order_detail', reference=order.reference)
    else:
        form = CheckoutForm(initial=initial)
    return render(request, 'store/checkout.html', {
        'form': form,
        'items': items,
        'subtotal': subtotal,
        'shipping': shipping,
        'total': subtotal + shipping,
        'free_shipping_threshold': FREE_SHIPPING_THRESHOLD,
    })


@login_required
def orders(request):
    return render(request, 'store/orders.html', {'orders': request.user.store_orders.all()})


@login_required
def order_detail(request, reference):
    order = get_object_or_404(Order.objects.prefetch_related('items'), reference=reference, user=request.user)
    return render(request, 'store/order_detail.html', {'order': order})


@login_required
def profile(request):
    customer_profile, _ = CustomerProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        user_form = UserProfileForm(request.POST, instance=request.user)
        profile_form = CustomerProfileForm(request.POST, instance=customer_profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('store:profile')
    else:
        user_form = UserProfileForm(instance=request.user)
        profile_form = CustomerProfileForm(instance=customer_profile)
    return render(request, 'store/profile.html', {'user_form': user_form, 'profile_form': profile_form})


def sign_up(request):
    if request.user.is_authenticated:
        return redirect('store:home')
    form = SignUpForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        CustomerProfile.objects.create(user=user)
        login(request, user)
        messages.success(request, 'Welcome to Pexo Market.')
        return redirect('store:home')
    return render(request, 'store/signup.html', {'form': form})


class StoreLoginView(LoginView):
    template_name = 'store/login.html'
    redirect_authenticated_user = True


class StoreLogoutView(LogoutView):
    pass
