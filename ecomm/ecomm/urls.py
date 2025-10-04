from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from app1 import views


urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', views.index, name='index'),  
    path('cart/', views.cart, name='cart'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('order-complete/', views.order_complete, name='order_complete'),
    path('place-order/', views.place_order, name='place_order'),
    path('product-detail/', views.product_detail, name='product_detail'),
    path('register/', views.register, name='register'),
    path('search-result/', views.search_result, name='search_result'),
    path('signin/', views.signin, name='signin'),
    path('store/', views.store, name='store'),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.BASE_DIR / "static")
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)