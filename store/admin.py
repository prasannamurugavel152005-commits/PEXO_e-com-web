from django.contrib import admin

from .models import Category, CustomerProfile, Order, OrderItem, Product, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ('name', 'slug')
	prepopulated_fields = {'slug': ('name',)}
	search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ('name', 'category', 'price', 'stock', 'available', 'featured')
	list_filter = ('category', 'available', 'featured')
	list_editable = ('price', 'stock', 'available', 'featured')
	search_fields = ('name', 'description')
	prepopulated_fields = {'slug': ('name',)}


class OrderItemInline(admin.TabularInline):
	model = OrderItem
	extra = 0
	readonly_fields = ('product', 'product_name', 'unit_price', 'quantity')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_display = ('reference', 'user', 'status', 'total', 'created_at')
	list_filter = ('status', 'created_at')
	search_fields = ('reference', 'user__username', 'user__email')
	readonly_fields = ('reference', 'subtotal', 'shipping', 'total', 'created_at')
	inlines = (OrderItemInline,)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
	list_display = ('product', 'user', 'rating', 'created_at')
	list_filter = ('rating', 'created_at')
	search_fields = ('product__name', 'user__username', 'title')


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'phone', 'city')
	search_fields = ('user__username', 'user__email', 'phone')
