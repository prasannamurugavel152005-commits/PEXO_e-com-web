import uuid

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.text import slugify


class Category(models.Model):
	name = models.CharField(max_length=80, unique=True)
	slug = models.SlugField(max_length=90, unique=True, blank=True)
	description = models.CharField(max_length=240, blank=True)

	class Meta:
		ordering = ['name']
		verbose_name_plural = 'categories'

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.name)
		super().save(*args, **kwargs)

	def __str__(self):
		return self.name


class Product(models.Model):
	category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
	name = models.CharField(max_length=180)
	slug = models.SlugField(max_length=200, unique=True, blank=True)
	description = models.TextField()
	price = models.DecimalField(
		max_digits=10,
		decimal_places=2,
		verbose_name='Price (INR)',
		help_text='Enter the selling price in Indian rupees.',
	)
	image_url = models.URLField(blank=True)
	stock = models.PositiveIntegerField(default=0)
	available = models.BooleanField(default=True)
	featured = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-featured', '-created_at']

	def save(self, *args, **kwargs):
		if not self.slug:
			base_slug = slugify(self.name)
			candidate = base_slug
			suffix = 2
			while Product.objects.filter(slug=candidate).exclude(pk=self.pk).exists():
				candidate = f'{base_slug}-{suffix}'
				suffix += 1
			self.slug = candidate
		super().save(*args, **kwargs)

	@property
	def average_rating(self):
		return self.reviews.aggregate(average=models.Avg('rating'))['average'] or 0

	def __str__(self):
		return self.name


class CustomerProfile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='store_profile')
	phone = models.CharField(max_length=30, blank=True)
	address = models.CharField(max_length=220, blank=True)
	city = models.CharField(max_length=100, blank=True)
	postal_code = models.CharField(max_length=20, blank=True)

	def __str__(self):
		return f'{self.user} profile'


class Review(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='product_reviews')
	rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
	title = models.CharField(max_length=120)
	body = models.TextField(max_length=1200)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-created_at']
		constraints = [models.UniqueConstraint(fields=['product', 'user'], name='one_review_per_product_user')]

	def __str__(self):
		return f'{self.rating}/5 for {self.product}'


class Order(models.Model):
	class Status(models.TextChoices):
		PLACED = 'placed', 'Placed'
		PROCESSING = 'processing', 'Processing'
		SHIPPED = 'shipped', 'Shipped'
		DELIVERED = 'delivered', 'Delivered'
		CANCELLED = 'cancelled', 'Cancelled'

	reference = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='store_orders')
	status = models.CharField(max_length=20, choices=Status.choices, default=Status.PLACED)
	address = models.CharField(max_length=220)
	city = models.CharField(max_length=100)
	postal_code = models.CharField(max_length=20)
	phone = models.CharField(max_length=30)
	notes = models.CharField(max_length=300, blank=True)
	subtotal = models.DecimalField(max_digits=10, decimal_places=2)
	shipping = models.DecimalField(max_digits=8, decimal_places=2, default=0)
	total = models.DecimalField(max_digits=10, decimal_places=2)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-created_at']

	def __str__(self):
		return f'Order {str(self.reference)[:8]}'


class OrderItem(models.Model):
	order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='order_items')
	product_name = models.CharField(max_length=180)
	unit_price = models.DecimalField(max_digits=10, decimal_places=2)
	quantity = models.PositiveIntegerField()

	@property
	def line_total(self):
		return self.unit_price * self.quantity

	def __str__(self):
		return f'{self.quantity} x {self.product_name}'
