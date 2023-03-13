from django.contrib import admin
from .models import Article, Favourite, Note

# Register your models here.

admin.site.register(Article)
admin.site.register(Favourite)
admin.site.register(Note)
