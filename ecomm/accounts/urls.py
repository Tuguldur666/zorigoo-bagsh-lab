from django.urls import path
from . import views

# Namespace тодорхойлно
app_name = 'accounts'

urlpatterns = [
    path('signin/', views.signin, name='signin'),
    path('register/', views.register, name='register'),
    path('logout/', views.signout, name='logout'),
]
