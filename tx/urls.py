from django.urls import path, include
from tx import views

app_name = 'tx'
urlpatterns = [
    path('', views.tx, name='tx_home'),
]