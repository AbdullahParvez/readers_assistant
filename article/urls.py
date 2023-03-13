'''url for article'''
from django.urls import path

from .views import ArticleCreate, ArticleView, add_favourite_word, create_note, get_note

app_name = 'article'

urlpatterns = [
    path('create/', ArticleCreate.as_view(), name='create_article'),
    path('detail/<int:pk>/', ArticleView.as_view(), name='view_article'),
    path('set_favourites/', add_favourite_word, name='set_favourites'),
    path('<int:article_id>/note_create/', create_note, name='note_create'),
    path('get_note/', get_note, name='get_note'),
]
