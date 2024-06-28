from django.urls import path

from .views.url_views import search_word, search_kanji, kanji_hover, KanjiListView, KanjiDetailView, KanjiUpdateView
from .views.api_views import GetKanjiDetails

app_name = 'kanji'

urlpatterns = [
    path("list/", KanjiListView.as_view(), name='kanji_list'),
    path('home/', search_word, name='home'),
    path('search/', search_kanji, name='kanji_search'),
    # path('search/<str:kanji>/', search_kanji_by_kanji, name='search_kanji_by_kanji'),
    path('hover/', kanji_hover, name='kanji_hover'),
    path('api/kanji_details/<str:kanji>/', GetKanjiDetails.as_view(), name='get_kanji_details'),
    path("<int:pk>/details/", KanjiDetailView.as_view(), name="kanji_detail"),
    path("<int:pk>/update/", KanjiUpdateView.as_view(), name="kanji_update"),
]
