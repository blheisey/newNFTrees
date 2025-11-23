from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Cart, CartItem 
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect
from django.urls import reverse


from django.shortcuts import render
from .models import Product

def product_list(request):
    # get the category from URL query parameter
    category = request.GET.get('category')
    
    if category:
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.all()
    
    # pass the distinct categories for the navbar
    nav_categories = Product.objects.values_list('category', flat=True).distinct()
    
    return render(request, 'shop/products.html', {
        'products': products,
        'nav_categories': nav_categories
    }) 

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'shop/product_detail.html', {'product': product})

def cart_view(request):
    cart = Cart.objects.filter(customer=request.user.customer).first()
    items = cart.cartitem_set.all() if cart else []
    return render(request, 'shop/cart.html', {'cart_items': items})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(customer=request.user.customer)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += 1
    item.save()
    return redirect(request.META.get('HTTP_REFERER', '')) # Previously: /shop/products/ This path does not exist

def remove_from_cart(request, product_id):
    cart = Cart.objects.filter(customer=request.user.customer).first()
    if cart:
        item = CartItem.objects.filter(cart=cart, product_id=product_id).first()
        if item:
            item.delete()
    return redirect(request.META.get('HTTP_REFERER', '/shop/cart/'))

@require_POST
def update_cart_item(request, product_id):
    new_qty = int(request.POST.get('quantity', 1))
    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(customer=request.user.customer)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if new_qty > 0:
        item.quantity = new_qty
        item.save()
    else:
        item.delete()  # remove item if quantity set to 0

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('shop:cart')))


