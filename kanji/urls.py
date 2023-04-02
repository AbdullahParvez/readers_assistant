from django.urls import path

from .views import kanji_hover

app_name = 'kanji'

urlpatterns = [
    path('hover/', kanji_hover, name='kanji_hover'),
]
