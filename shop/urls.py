from django.urls import path
from . import views

app_name = "shop"

urlpatterns = [
    path("", views.product_list, name="product_list"),  # /shop/ → all products
    path('<int:pk>/', views.product_detail, name='product_detail'),  # new
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
]
