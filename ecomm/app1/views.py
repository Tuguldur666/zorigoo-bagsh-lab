from django.shortcuts import render
from app1.models import Category
from app1.models import Product

def get_categories():
    return Category.objects.all()


def index(request):
    categories = get_categories()
    products = Product.objects.filter(is_available=True)
    return render(request, 'index.html', {'categories': categories , 'products': products})

def store(request):
    categories = get_categories()
    products = Product.objects.filter(is_available=True)
    return render(request, 'store.html', {'categories': categories ,  'products': products})

def cart(request):
    categories = get_categories()
    return render(request, 'cart.html', {'categories': categories})

def dashboard(request):
    categories = get_categories()
    return render(request, 'dashboard.html', {'categories': categories})

def order_complete(request):
    categories = get_categories()
    return render(request, 'order_complete.html', {'categories': categories})

def place_order(request):
    categories = get_categories()
    return render(request, 'place_order.html', {'categories': categories})

def product_detail(request):
    categories = get_categories()
    return render(request, 'product_detail.html', {'categories': categories})

def register(request):
    categories = get_categories()
    return render(request, 'register.html', {'categories': categories})

def search_result(request):
    categories = get_categories()
    return render(request, 'search_result.html', {'categories': categories})

def signin(request):
    categories = get_categories()
    return render(request, 'signin.html', {'categories': categories})
