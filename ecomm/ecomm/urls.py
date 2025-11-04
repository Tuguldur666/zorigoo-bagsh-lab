from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from app1 import views
from carts import views


urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', views.index, name='index'),  
    path('cart/', views.cart, name='cart'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('order-complete/', views.order_complete, name='order_complete'),
    path('place-order/', views.place_order, name='place_order'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('register/', views.register, name='register'),
    path('search-result/', views.search_result, name='search_result'),
    path('signin/', views.signin, name='signin'),
    path('store/', views.store, name='store'),
    path('store/category/<slug:category_slug>/', views.store, name='products_by_category'),
    path('', views.cart, name='cart'),
    path('cart/', include('carts.urls')),
    path('add/<int:product_id>/', views.add_cart, name='add_cart'),
    path('remove/<int:product_id>/', views.remove_cart, name='remove_cart'),
    path('remove_item/<int:product_id>/', views.remove_cart_item, name='remove_cart_item'),

]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.BASE_DIR / "static")
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)