from django.urls import path

from .views.url_views import search_word, search_kanji, kanji_hover
from .views.api_views import GetKanjiDetails

app_name = 'kanji'

urlpatterns = [
    path('home/', search_word, name='kanji_show'),
    path('kanji/search/', search_kanji, name='kanji_search'),
    path('hover/', kanji_hover, name='kanji_hover'),
    path('api/kanji_details/<str:kanji>/', GetKanjiDetails.as_view(), name='get_kanji_details'),
]
