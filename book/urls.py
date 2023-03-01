'''url for book'''
from django.urls import path

from .views import create_book, details_book, ChapterCreate, ChapterDetails, add_favourite_word

app_name = 'book'

urlpatterns = [
    # path('create/', BookCreate.as_view(), name='create'),
    path('create/', create_book, name='create'),
    path('details/<int:id>/', details_book, name='details'),
    path('<int:book_id>/chapter/create/', ChapterCreate.as_view(), name='chapter_create'),
    path('chapter/details/<int:pk>/', ChapterDetails.as_view(), name='chapter_details'),
    path('set_favourites/', add_favourite_word, name='set_favourites'),
]
