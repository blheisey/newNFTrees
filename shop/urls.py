from django.urls import path

from . import views

app_name = "shop"

urlpatterns = [
    path("", views.product_list, name="product_list"),  # /shop/ → all products
    path('<int:pk>/', views.product_detail, name='product_detail'),  # new
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:product_id>/', views.update_cart_item, name='update_cart_item'),
    path('nfts/', views.my_nfts, name='my_nfts'),  # User's purchased NFTs
    path('download/<int:product_id>/', views.download_nft_image, name='download_nft'),  # Secure download


]
