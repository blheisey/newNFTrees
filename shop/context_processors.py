from .models import Product, Cart, CartItem
from accounts.models import Customer
from django.db.models import Sum

def product_categories(request):
    # Return distinct category values from the Product table
    categories = Product.objects.values_list("category", flat=True).distinct()
    return {"nav_categories": categories}

from shop.models import Cart, CartItem
from django.db.models import Sum

def cart_count(request):
    # Unauthenticated user → no cart
    if not request.user.is_authenticated:
        return {"cart_count": 0}

    # Get the linked Customer object
    try:
        customer = request.user.customer
    except Customer.DoesNotExist:
        return {"cart_count": 0}

    # Retrieve this customer's cart
    try:
        cart = Cart.objects.get(customer=customer)
    except Cart.DoesNotExist:
        return {"cart_count": 0}

    # Count all quantities inside the cart
    total_items = (
        CartItem.objects.filter(cart=cart).aggregate(Sum("quantity"))["quantity__sum"]
        or 0
    )

    return {"cart_count": total_items}
