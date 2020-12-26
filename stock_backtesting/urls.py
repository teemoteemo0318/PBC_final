from django.urls import path, include
from stock_backtesting import views

app_name = 'stock_backtesting'
urlpatterns = [
    path('', views.stock_backtesting, name='stock_backtesting_home'),
]