from django.urls import path, include
from products import views

app_name = 'products'
urlpatterns = [
    path('', views.products, name='products_home'),
]