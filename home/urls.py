from django.urls import path
from home import views

home_urlpatterns = [
    path('', views.home, name='home'),
]