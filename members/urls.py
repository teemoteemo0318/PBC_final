from django.urls import path, include
from members import views

app_name = 'members'
urlpatterns = [
    path('', views.members, name='members_home'),
]