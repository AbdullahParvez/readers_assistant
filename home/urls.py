'''url for home'''
from django.urls import path

from .views import index, policy, home

app_name = 'home'

urlpatterns = [
    path('', home, name='home'),
    path('index/', index, name='index'),
    path('policy/', policy, name='policy'),
]
