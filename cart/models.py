from django.db import models
from django.conf import settings
from products.models import Product

# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart {self.id}"

    def get_total_price(self):
        return sum(item.total_price for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    color = models.CharField(max_length=50, null=True, blank=True)
    size = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        variation_details = []
        if self.color:
            variation_details.append(self.color)
        if self.size:
            variation_details.append(self.size)
        
        variation_str = f" - {' '.join(variation_details)}" if variation_details else ""
        return f"{self.quantity} x {self.product.name}{variation_str}"

    @property
    def total_price(self):
        # Check if the variation has a price override
        variation = self.product.variations.filter(
            color=self.color, 
            size=self.size
        ).first()
        
        if variation and variation.price_override:
            return self.quantity * variation.price_override
        
        return self.quantity * self.product.price

    class Meta:
        unique_together = ['cart', 'product', 'color', 'size']
