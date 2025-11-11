from django.shortcuts import render, get_object_or_404, redirect
from app1.models import Product
from .models import Cart, CartItem


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        request.session.create()
        cart = request.session.session_key  
    return cart


def add_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(cart_id=_cart_id(request))

    cart_item, created = CartItem.objects.get_or_create(product=product, cart=cart)
    
    if not created:
        if cart_item.quantity < product.stock:  
            cart_item.quantity += 1
            cart_item.save()
        else:
            from django.contrib import messages
            messages.warning(request, f"Only {product.stock} items available in stock.")
    else:
        if product.stock > 0:
            cart_item.quantity = 1
            cart_item.save()
        else:
            messages.warning(request, "Product is out of stock.")

    return redirect('cart')


def remove_cart(request, product_id):
    cart = get_object_or_404(Cart, cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = get_object_or_404(CartItem, product=product, cart=cart)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart')


def remove_cart_item(request, product_id):
    cart = get_object_or_404(Cart, cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = get_object_or_404(CartItem, product=product, cart=cart)
    cart_item.delete()
    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for item in cart_items:
            total += item.product.price * item.quantity
            quantity += item.quantity
    except Cart.DoesNotExist:
        cart_items = []

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
    }
    return render(request, 'cart.html', context)
