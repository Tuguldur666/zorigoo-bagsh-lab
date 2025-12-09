from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from app1 import views as app1_views
from carts import views as cart_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # --- App1 views ---
    path('', app1_views.index, name='index'),
    path('dashboard/', app1_views.dashboard, name='dashboard'),
    path('order-complete/', app1_views.order_complete, name='order_complete'),
    path('place-order/', app1_views.place_order, name='place_order'),
    path('product/<int:product_id>/', app1_views.product_detail, name='product_detail'),
    path('search-result/', app1_views.search_result, name='search_result'),
    path('store/', app1_views.store, name='store'),
    path('submit_review/<int:product_id>/', app1_views.submit_review, name='submit_review'),
    path('store/search/', app1_views.search, name='store_search'),
    path('store/category/<slug:category_slug>/', app1_views.store, name='products_by_category'),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('accounts/', include('allauth.urls')),
    # --- Cart views (no carts.urls used) ---s
    path('cart/', cart_views.cart, name='cart'),
    path('add/<int:product_id>/', cart_views.add_cart, name='add_cart'),
    path('remove/<int:product_id>/', cart_views.remove_cart, name='remove_cart'),
    path('remove_item/<int:product_id>/', cart_views.remove_cart_item, name='remove_cart_item'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.BASE_DIR / "static")
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
