from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Category, Order, Product, Review


class StoreFlowTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Home & Living')
        self.product = Product.objects.create(
            category=self.category,
            name='Everyday Mug',
            description='A durable ceramic mug for everyday coffee.',
            price=Decimal('12.50'),
            stock=6,
        )
        self.user = User.objects.create_user(username='shopper', password='test-password-strong')

    def test_home_and_catalog_render(self):
        home_response = self.client.get(reverse('store:home'))
        catalog_response = self.client.get(reverse('store:products'), {'q': 'mug'})

        self.assertEqual(home_response.status_code, 200)
        self.assertContains(home_response, 'Find your')
        self.assertEqual(catalog_response.status_code, 200)
        self.assertContains(catalog_response, self.product.name)
        self.assertContains(catalog_response, '₹12.50')

    def test_external_cart_return_url_is_rejected(self):
        response = self.client.post(reverse('store:add_to_cart', args=[self.product.pk]), {
            'quantity': '1',
            'next': 'https://example.com/',
        })

        self.assertRedirects(response, reverse('store:cart'))

    def test_checkout_creates_order_and_decrements_stock(self):
        self.client.force_login(self.user)
        self.client.post(reverse('store:add_to_cart', args=[self.product.pk]), {'quantity': '2'})
        response = self.client.post(reverse('store:checkout'), {
            'address': '12 Market Street',
            'city': 'Portland',
            'postal_code': '97201',
            'phone': '555-0140',
            'notes': '',
        })

        order = Order.objects.get(user=self.user)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(order.total, Decimal('74.00'))
        self.assertEqual(order.items.get().quantity, 2)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 4)
        self.assertEqual(self.client.session.get('cart'), {})

    def test_customer_can_submit_one_review_per_product(self):
        self.client.force_login(self.user)
        review_url = reverse('store:add_review', args=[self.product.slug])
        payload = {'rating': '5', 'title': 'A daily favorite', 'body': 'Feels lovely and sturdy.'}

        first_response = self.client.post(review_url, payload)
        second_response = self.client.post(review_url, {**payload, 'title': 'Still a favorite'})

        self.assertEqual(first_response.status_code, 302)
        self.assertEqual(second_response.status_code, 302)
        self.assertEqual(Review.objects.filter(product=self.product, user=self.user).count(), 1)
        self.assertEqual(Review.objects.get(product=self.product, user=self.user).title, 'Still a favorite')

    def test_account_cart_checkout_and_order_templates_render(self):
        self.assertEqual(self.client.get(reverse('store:login')).status_code, 200)
        self.assertEqual(self.client.get(reverse('store:signup')).status_code, 200)
        self.assertEqual(self.client.get(reverse('store:product_detail', args=[self.product.slug])).status_code, 200)
        self.assertEqual(self.client.get(reverse('store:cart')).status_code, 200)

        self.client.force_login(self.user)
        self.client.post(reverse('store:add_to_cart', args=[self.product.pk]), {'quantity': '1'})
        self.assertEqual(self.client.get(reverse('store:checkout')).status_code, 200)
        self.assertEqual(self.client.get(reverse('store:profile')).status_code, 200)
        self.assertEqual(self.client.get(reverse('store:orders')).status_code, 200)

        order = Order.objects.create(
            user=self.user,
            address='12 Market Street',
            city='Portland',
            postal_code='97201',
            phone='555-0140',
            subtotal=Decimal('12.50'),
            shipping=Decimal('49.00'),
            total=Decimal('61.50'),
        )
        response = self.client.get(reverse('store:order_detail', args=[order.reference]))
        self.assertEqual(response.status_code, 200)
