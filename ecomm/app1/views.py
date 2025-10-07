from django.shortcuts import render, get_object_or_404
from app1.models import Category, Product
import sqlite3 as sql

def index(request):
    con = sql.connect('db.sqlite3')
    cur = con.cursor()
    cur.execute('''
        SELECT * FROM app1_product 
        WHERE is_available=1 
        ORDER BY id DESC 
        LIMIT 5
    ''') 
    products = cur.fetchall()
    product_count = len(products)
    con.close()
    context = {
        'products': products,
        'product_count': product_count
    }
    return render(request, 'index.html', context)



def store(request, category_slug=None):
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category, is_available=True)
    else:
        products = Product.objects.filter(is_available=True)
    return render(request, 'store.html', {'products': products})

def cart(request):
    return render(request, 'cart.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def order_complete(request):
    return render(request, 'order_complete.html')

def place_order(request):
    return render(request, 'place_order.html')

def product_detail(request):
    return render(request, 'product_detail.html')

def register(request):
    return render(request, 'register.html')

def search_result(request):
    return render(request, 'search_result.html')

def signin(request):
    return render(request, 'signin.html')
