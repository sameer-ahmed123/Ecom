import random
from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth.models import User

class Category(models.Model):
    """Category to classify products (e.g., Electronics, Clothing, Home)."""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)  # Allow blank so we can auto-generate

    def save(self, *args, **kwargs):
        if not self.slug or self.name_has_changed():
            self.slug = self._generate_unique_slug()
        super().save(*args, **kwargs)

    def name_has_changed(self):
        """Check if the category name has changed (only if updating)."""
        if self.pk:
            original = Category.objects.get(pk=self.pk)
            return original.name != self.name
        return True

    def _generate_unique_slug(self):
        """Generate a unique slug by appending random numbers if necessary."""
        base_slug = slugify(self.name)
        slug = base_slug
        counter = 1
        while Category.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        return slug

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Tags for products (e.g., 'summer', 'bestseller')."""
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    """Enhanced Product Model for an e-commerce website."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="products")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    stock_quantity = models.PositiveIntegerField(default=0)  # Stock count
    is_in_stock = models.BooleanField(default=True)  # Automatically updated

    main_image = models.ImageField(upload_to="product_images/", blank=True, null=True)  # 🖼️ Main image

    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Auto-set slug
        if not self.slug:
            base_slug = slugify(self.name)
            self.slug = self._generate_unique_slug(base_slug)
        
        # Auto-update stock status
        self.is_in_stock = self.stock_quantity > 0

        super().save(*args, **kwargs)

    def _generate_unique_slug(self, base_slug):
        slug = base_slug
        while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f"{base_slug}-{random.randint(1000, 9999)}"
        return slug

    def update_sale_price(self, new_sale_price):
        self.sale_price = new_sale_price
        self.save()

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name


class ProductVariant(models.Model):
    """Handles different sizes and colors of a product."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="variants")
    size = models.CharField(max_length=50, blank=True, null=True)  # Example: S, M, L, XL
    color = models.CharField(max_length=50, blank=True, null=True)  # Example: Red, Blue

    stock_quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.product.name} - {self.color} - {self.size}"


class ProductReview(models.Model):
    """Allows users to review products."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=1)  # Rating from 1-5
    review = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.rating}⭐)"
