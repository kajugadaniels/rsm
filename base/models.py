from django.db import models
from django.utils import timezone
from django.utils.text import slugify

class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Automatically generate slug if not provided
        if not self.slug:
            self.slug = self.generate_unique_slug()
        super(Product, self).save(*args, **kwargs)

    def generate_unique_slug(self):
        """
        Generates a unique slug from the product's name.
        If the slug already exists, appends a numerical suffix to make it unique.
        """
        base_slug = slugify(self.name)
        slug = base_slug
        counter = 1
        while Product.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        return slug
