import random
from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.functions import Lower
from django.db.models import Max


# -------------------------------
# Category and Tag Models
# -------------------------------

class Category(models.Model):
    """Category to classify products (e.g., Electronics, Clothing, Home)."""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug or self.name_has_changed():
            self.slug = self._generate_unique_slug()
        super().save(*args, **kwargs)

    def name_has_changed(self):
        if self.pk:
            original = Category.objects.get(pk=self.pk)
            return original.name != self.name
        return True

    def _generate_unique_slug(self):
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
    name = models.CharField(
        max_length=50,
        unique=True,
        help_text="Case-insensitive uniqueness is enforced"
    )

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower('name'),
                name='tag_name_unique_case_insensitive'
            ),
        ]

# -------------------------------
# ProductVariant Model
# -------------------------------


VARIANT_TYPE_CHOICES = (
    ('physical', 'Physical'),
    ('digital', 'Digital'),
)


class ProductVariant(models.Model):
    """Product variants that can be either physical or digital."""
    product = models.ForeignKey(
        'Product', on_delete=models.CASCADE, related_name="variants", db_index=True
    )
    variant_type = models.CharField(
        max_length=20,
        choices=VARIANT_TYPE_CHOICES,
        default='physical'
    )
    variant_description = models.TextField(
        max_length=500, blank=True, null=True)
    # Fields for physical products
    size = models.CharField(max_length=50, blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    weight = models.DecimalField(
        max_digits=6, decimal_places=2, blank=True, null=True)
    dimensions = models.CharField(max_length=100, blank=True, null=True)
    # Field for digital products
    file = models.FileField(
        upload_to='digital_files/',
        blank=True,
        null=True,
        help_text="Only required if variant is Digital"
    )
    variant_image = models.ImageField(
        upload_to="product_images/variant_images/",
        blank=True,
        null=True
    )
    # Common fields
    stock_quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Leave blank to use the product's base price."
    )

    @property
    def final_price(self):
        return self.price if self.price is not None else self.product.base_price

    @property
    def is_in_stock(self):
        # For digital variants, we consider them always in stock.
        if self.variant_type == 'digital':
            return True
        return self.stock_quantity > 0

    def __str__(self):
        details = [self.variant_type.capitalize()]
        if self.variant_type == 'physical':
            if self.size or self.color:
                details.append(f"{self.size or ''} {self.color or ''}".strip())
        return f"Variant of {self.product.name} - {' | '.join(details) or 'Standard'}"

    class Meta:
        unique_together = [['product', 'size', 'color']]

# -------------------------------
# Product Model
# -------------------------------


class Product(models.Model):
    """Enhanced Product Model for a modern e-commerce website."""
    PRODUCT_TYPES = (
        ('physical', 'Physical Product'),
        ('digital', 'Digital Product'),
    )
    product_type = models.CharField(
        max_length=10, choices=PRODUCT_TYPES, default='physical')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="products"
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )
    tags = models.ManyToManyField(Tag, blank=True)
    # Basic details
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    brand = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(
        help_text="Short description of the product")
    detailed_description = models.TextField(
        blank=True,
        null=True,
        help_text="Detailed product description with features, specifications, etc."
    )
    features = models.TextField(
        blank=True,
        null=True,
        help_text="List key features or bullet points (e.g., HTML or Markdown)"
    )
    base_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Base price if not specified in product variants"
    )
    sale_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )
    main_image = models.ImageField(
        upload_to="product_images/",
        blank=True,
        null=True
    )
    # New field: Allow digital products to have an associated file
    digital_file = models.FileField(
        upload_to='digital_files/',
        blank=True,
        null=True,
        help_text="Upload a file if this is a digital product"
    )
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    stock_quantity = models.PositiveIntegerField(
        default=0,
        help_text="Stock quantity for products without variants"
    )

    @property
    def has_variants(self):
        return self.variants.exists()

    @property
    def total_stock(self):
        if self.variants.exists():
            total_of_variants = sum(
                variant.stock_quantity for variant in self.variants.all())
            return self.stock_quantity + total_of_variants
        return self.stock_quantity

    @property
    def is_in_stock(self):
        self.has_variants
        if self.product_type == "digital":
            return True
        return self.stock_quantity > 0

    @property
    def max_variant_price(self):
        max_price = self.variants.aggregate(Max("price"))["price__max"]
        return max_price if max_price is not None else self.base_price

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            self.slug = self._generate_unique_slug(base_slug)
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

# -------------------------------
# ProductReview Model
# -------------------------------


class ProductReview(models.Model):
    """Allows users to review products."""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="product_reviews"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"
    )
    rating = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    review = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.rating}⭐)"
