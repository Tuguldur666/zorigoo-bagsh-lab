from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q, Avg
from django.contrib import messages
import sqlite3 as sql

from app1.models import Product, Category, ReviewRating
from django.contrib.auth.decorators import login_required


# --------------------
# INDEX PAGE
# --------------------
from django.db.models import Avg
from app1.models import Product, ReviewRating

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
    con.close()

    # Prepare list with rating info
    product_list = []
    for prod in products:
        prod_id = prod[0]  # assuming ID is first column
        # Fetch average rating using ORM
        avg = ReviewRating.objects.filter(product_id=prod_id).aggregate(avg_rating=Avg('rating'))['avg_rating']
        average_rating = float(avg or 0)
        full_stars = int(average_rating)
        half_star = 1 if (average_rating - full_stars) >= 0.5 else 0
        empty_stars = 5 - full_stars - half_star

        product_list.append({
            'data': prod,  # original tuple
            'average_rating': average_rating,
            'full_stars': range(full_stars),
            'half_star': half_star,
            'empty_stars': range(empty_stars),
        })

    context = {
        'products': product_list,
        'product_count': len(products)
    }
    return render(request, 'index.html', context)


# --------------------
# STORE PAGE
# --------------------
def store(request, category_slug=None):
    keyword = request.GET.get('keyword')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    products = Product.objects.filter(is_available=True)

    category = None
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    if keyword:
        products = products.filter(product_name__icontains=keyword)

    if min_price:
        try:
            products = products.filter(price__gte=int(min_price))
        except ValueError:
            pass

    if max_price:
        try:
            products = products.filter(price__lte=int(max_price))
        except ValueError:
            pass

    # Add rating info to each product
    product_list = []
    for product in products:
        avg = ReviewRating.objects.filter(product=product).aggregate(avg_rating=Avg('rating'))['avg_rating']
        average_rating = float(avg or 0)
        full_stars = int(average_rating)
        half_star = 1 if (average_rating - full_stars) >= 0.5 else 0
        empty_stars = 5 - full_stars - half_star

        product_list.append({
            'product': product,
            'average_rating': average_rating,
            'full_stars': range(full_stars),
            'half_star': half_star,
            'empty_stars': range(empty_stars),
        })

    paginator = Paginator(product_list, 5)
    page_number = request.GET.get('page')
    paged_products = paginator.get_page(page_number)

    context = {
        'products': paged_products,
        'keyword': keyword,
        'category': category,
        'min_price': min_price,
        'max_price': max_price,
        'product_count': len(product_list),
    }
    return render(request, 'store.html', context)

# --------------------
# SEARCH PAGE
# --------------------
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


# --------------------
# OTHER PAGES
# --------------------
def cart(request):
    return render(request, 'cart.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def order_complete(request):
    return render(request, 'order_complete.html')

def place_order(request):
    return render(request, 'place_order.html')

def search_result(request):
    return render(request, 'search_result.html')



# --------------------
# PRODUCT DETAIL + REVIEWS
# --------------------
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    avg = ReviewRating.objects.filter(product=product).aggregate(avg_rating=Avg('rating'))['avg_rating']
    average_rating = float(avg or 0)

    full_stars = int(average_rating)
    half_star = 1 if (average_rating - full_stars) >= 0.5 else 0
    empty_stars = 5 - full_stars - half_star

    comments = ReviewRating.objects.filter(product=product).order_by('-created_date')

    context = {
        'product': product,
        'average_rating': average_rating,
        'full_stars': range(full_stars),
        'half_star': half_star,
        'empty_stars': range(empty_stars),
        'comments': comments,
    }
    return render(request, 'product-detail.html', context)
# --------------------
# SUBMIT REVIEW
# --------------------
@login_required
def submit_review(request, product_id):
    product = Product.objects.get(id=product_id)

    if request.method == "POST":
        title = request.POST.get('title')
        review = request.POST.get('review')
        rate = request.POST.get('rate')

        try:
            existing_review = ReviewRating.objects.get(user=request.user, product=product)

            existing_review.title = title
            existing_review.review = review
            existing_review.rating = rate
            existing_review.ip = request.META.get('REMOTE_ADDR')
            existing_review.save()

            messages.success(request, "Your review has been updated.")

        except ReviewRating.DoesNotExist:
            new_review = ReviewRating(
                product=product,
                user=request.user,
                title=title,
                review=review,
                rating=rate,
                ip=request.META.get('REMOTE_ADDR'),
            )
            new_review.save()

            messages.success(request, "Thank you! Your review has been submitted.")

    return redirect('product_detail', product_id=product.id)
