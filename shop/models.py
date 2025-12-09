from accounts.models import Customer
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50, choices=[('tree','Tree'), ('ornament','Ornament'), ('nft','NFT')])
    price = models.DecimalField(max_digits=10, decimal_places=2)
    inventory = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products/', blank=True)

    def __str__(self):
        return self.name

    def user_owns_nft(self, user):
        """Check if user has purchased this NFT"""
        if not user.is_authenticated or self.category != 'nft':
            return False
    
        # Check if user has a customer profile
        try:
            customer = user.customer
        except AttributeError:
            return False
    
        return OrderItem.objects.filter(
            order__customer=customer,
            product=self,
            order__created_at__isnull=False  # Ensure order is completed
        ).exists()

class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)  # Make nullable temporarily
    product_name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1) 
