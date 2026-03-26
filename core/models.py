from django.db import models
from django.conf import settings
from django.urls import reverse
from django.core.validators import MinValueValidator
from decimal import Decimal


class Product(models.Model):
    CATEGORY_CHOICES = (
        ("SOLAR_PANELS", "Solar Panels"),
        ("INVERTERS", "Inverters"),
        ("BATTERIES", "Batteries"),
        ("WATER_HEATERS", "Water Heaters"),
        ("ACCESSORIES", "Accessories"),
        ("MOUNTING", "Mounting Structures"),
        ("CLEANING", "Cleaning Systems"),
    )
    
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default="ACCESSORIES")
    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))]
    )
    image = models.ImageField(upload_to="products/", default="products/default.png")
    is_active = models.BooleanField(default=True)
    stock_quantity = models.IntegerField(default=0)
    min_order_quantity = models.PositiveIntegerField(default=1)
    max_order_quantity = models.PositiveIntegerField(null=True, blank=True)
    slug = models.SlugField(
        unique=True, null=True, blank=True
    )  # <-- add null=True and blank=True for existing rows

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"slug": self.slug})


class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.email}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"

    def get_total_price(self):
        return self.product.price * self.quantity


class Order(models.Model):
    PAYMENT_METHODS = (
        ("COD", "Cash on Delivery"),
        ("ONLINE", "Online Payment"),  # For future use
    )

    STATUS_CHOICES = (
        ("PLACED", "Placed"),
        ("PROCESSING", "Processing"),
        ("COMPLETED", "Completed"),
        ("CANCELLED", "Cancelled"),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(
        max_length=20, choices=PAYMENT_METHODS, default="COD"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PLACED")

    def __str__(self):
        return f"Order #{self.id} by {self.user.email}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"
