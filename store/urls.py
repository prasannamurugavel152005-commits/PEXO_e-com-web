from django.urls import path

from . import views

app_name = 'store'

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('products/<slug:slug>/', views.product_detail, name='product_detail'),
    path('products/<slug:slug>/review/', views.add_review, name='add_review'),
    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('account/login/', views.StoreLoginView.as_view(), name='login'),
    path('account/logout/', views.StoreLogoutView.as_view(), name='logout'),
    path('account/signup/', views.sign_up, name='signup'),
    path('account/profile/', views.profile, name='profile'),
    path('account/orders/', views.orders, name='orders'),
    path('account/orders/<uuid:reference>/', views.order_detail, name='order_detail'),
]