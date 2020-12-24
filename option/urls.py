from django.urls import path, include
from option import views

app_name = 'option'
urlpatterns = [
    path('', views.option, name='option_home'),
]