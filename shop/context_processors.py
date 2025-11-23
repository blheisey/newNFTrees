from .models import Product

def product_categories(request):
    # Return distinct category values from the Product table
    categories = Product.objects.values_list("category", flat=True).distinct()
    return {"nav_categories": categories}