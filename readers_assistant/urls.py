from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from drf_spectacular.views import(
    SpectacularAPIView,
    SpectacularSwaggerView,
)
from .views.url_views import get_word_meaning
from .views.api_views import GetVocabDetails



urlpatterns = [
    path('api/schema/', SpectacularAPIView.as_view(), name='api_schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='api_schema'), name='api_docs'),
    path('admin/', admin.site.urls),
    # path('accounts/', include('django.contrib.auth.urls')),
    path('tinymce/', include('tinymce.urls')),
    path('user/', include('user.urls')),
    path('', include('home.urls')),
    path('article/', include('article.urls')),
    path('book/', include('book.urls')),
    path('kanji/', include('kanji.urls')),
    path('word/meaning/', get_word_meaning, name='get_word_meaning'),
    path('api/vocab_details/<str:vocab>/', GetVocabDetails.as_view(), name='get_word_details'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
