import mimetypes
import os

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import (FileResponse, Http404, HttpResponse,
                         HttpResponseRedirect)
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from .models import Cart, CartItem, OrderItem, Product


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
    
    # Check if user owns this NFT (for template context)
    user_owns_nft = False
    if request.user.is_authenticated and product.category == 'nft':
        user_owns_nft = product.user_owns_nft(request.user)
    
    return render(request, 'shop/product_detail.html', {
        'product': product,
        'user_owns_nft': user_owns_nft
    })

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
    return redirect(request.META.get('HTTP_REFERER', '/shop/products/'))

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


@login_required
def download_nft_image(request, product_id):
    """
    Secure NFT image download - only for customers who purchased the NFT
    """
    product = get_object_or_404(Product, pk=product_id, category='nft')
    
    # Check if user has customer profile
    try:
        customer = request.user.customer
    except AttributeError:
        raise Http404("Customer profile required")
    
    # Check if user owns this NFT
    if not product.user_owns_nft(request.user):
        raise Http404("You don't have permission to download this NFT")
    
    # Check if product has an image
    if not product.image:
        raise Http404("Image not found")
    
    # Get the file path
    file_path = product.image.path
    
    if not os.path.exists(file_path):
        raise Http404("Image file not found")
    
    # Determine content type
    content_type, _ = mimetypes.guess_type(file_path)
    if content_type is None:
        content_type = 'application/octet-stream'
    
    # Create response with file
    response = FileResponse(
        open(file_path, 'rb'),
        content_type=content_type,
        as_attachment=True,
        filename=f"{product.name}_NFT.{product.image.name.split('.')[-1]}"
    )
    
    return response


@login_required
def my_nfts(request):
    """
    Display user's purchased NFTs with download links
    """
    # Check if user has customer profile
    try:
        customer = request.user.customer
    except AttributeError:
        return render(request, 'shop/my_nfts.html', {
            'purchased_nfts': [],
            'error_message': "Customer profile required to view NFTs."
        })
    
    # Get all NFTs purchased by the user
    purchased_nfts = Product.objects.filter(
        orderitem__order__customer=customer,
        category='nft'
    ).distinct()
    
    return render(request, 'shop/my_nfts.html', {
        'purchased_nfts': purchased_nfts
    })


