'''url for home'''
from django.urls import path

from .views import home, policy

app_name = 'home'

urlpatterns = [
    path('', home, name='home'),
    path('policy/', policy, name='policy'),
]
