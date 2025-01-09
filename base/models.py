from account.models import *
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

class Client(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, unique=True)
    destination = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.phone_number})"

    def save(self, *args, **kwargs):
        super(Client, self).save(*args, **kwargs)

class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    orderId = models.CharField(max_length=10, unique=True, editable=False)
    destination = models.CharField(max_length=255, null=True, blank=True)
    addedBy = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders_added')
    updatedBy = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders_updated')
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.orderId

    def save(self, *args, **kwargs):
        if not self.orderId:
            self.orderId = self.generate_order_id()
        super(Order, self).save(*args, **kwargs)
        self.calculate_grand_total()

    def generate_order_id(self):
        """
        Generates a unique order ID starting with 'ORD', followed by a letter starting from 'A',
        and ending with a three-digit number (e.g., ORDA001).
        """
        last_order = Order.objects.all().order_by('id').last()
        if not last_order:
            return 'ORDA001'

        last_order_id = last_order.orderId
        if len(last_order_id) != 7 or not last_order_id.startswith('ORD'):
            return 'ORDA001'

        letter = last_order_id[3]
        number = int(last_order_id[4:7])

        if number < 999:
            number += 1
        else:
            # Reset number and increment letter
            number = 1
            letter = chr(ord(letter) + 1) if letter < 'Z' else 'A'

        return f'ORD{letter}{number:03d}'

    def calculate_grand_total(self):
        """
        Calculates the grand total by summing up all total_price from related OrderProduct instances.
        """
        self.grand_total = self.order_products.aggregate(total=models.Sum('total_price'))['total'] or 0.00
        super(Order, self).save(update_fields=['grand_total'])

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.FloatField()
    quantity = models.PositiveIntegerField()
    total_size = models.FloatField(editable=False)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def __str__(self):
        return f"{self.product.name} x {self.quantity} for {self.order.orderId}"

    def save(self, *args, **kwargs):
        self.total_size = self.size * self.quantity
        self.total_price = self.size * self.unit_price
        super(OrderProduct, self).save(*args, **kwargs)
        self.order.calculate_grand_total()

    def delete(self, *args, **kwargs):
        super(OrderProduct, self).delete(*args, **kwargs)
        self.order.calculate_grand_total()