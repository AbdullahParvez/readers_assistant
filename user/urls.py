'''url for book'''
from django.urls import path

from .views import login_page, login, register, logout

app_name = 'user'

urlpatterns = [
    # path('create/', BookCreate.as_view(), name='create'),
    path('login_page/', login_page, name='login_page'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('register/', register, name='register'),
]