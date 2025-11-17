from django import template
register = template.Library()

@register.filter
def multiply(qty, price):
    return qty * price

@register.filter
def sum_total(cart_items):
    return sum(item.quantity * item.product.price for item in cart_items)