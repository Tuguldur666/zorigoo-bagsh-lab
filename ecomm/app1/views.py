from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q  # Q объектыг импортолно
from app1.models import Product, Category
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


from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from app1.models import Product, Category

def store(request, category_slug=None):
    keyword = request.GET.get('keyword')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    products = Product.objects.filter(is_available=True)  # эхлээд бүх боломжит бүтээгдэхүүн

    category = None
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)  # зөвхөн тухайн категори

    if keyword:
        products = products.filter(
            Q(product_name__icontains=keyword) 
        )

    if min_price:
        try:
            products = products.filter(price__gte=int(min_price))
        except ValueError:
            pass  # буруу тоо орсон бол filter хийхгүй

    if max_price:
        try:
            products = products.filter(price__lte=int(max_price))
        except ValueError:
            pass

    paginator = Paginator(products, 5)
    page_number = request.GET.get('page')
    paged_products = paginator.get_page(page_number)

    context = {
        'products': paged_products,
        'keyword': keyword,
        'category': category,
        'min_price': min_price,
        'max_price': max_price,
        'product_count': products.count(),
    }
    return render(request, 'store.html', context)



def search(request):
    keyword = request.GET.get('keyword') 
    products = []
    product_count = 0

    if keyword:
        products = Product.objects.filter(
            Q(product_name__icontains=keyword),
            is_available=True
        )
        product_count = products.count()

    context = {
        'products': products,
        'product_count': product_count,
        'keyword': keyword,
    }
    return render(request, 'store.html', context)

def cart(request):
    return render(request, 'cart.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def order_complete(request):
    return render(request, 'order_complete.html')

def place_order(request):
    return render(request, 'place_order.html')
    
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product-detail.html', {'product': product})


def search_result(request):
    return render(request, 'search_result.html')


