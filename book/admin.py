from django.contrib import admin
from .models import Book, Chapter, Favourite, Note

# Register your models here.

admin.site.register(Book)
admin.site.register(Chapter)
admin.site.register(Favourite)
admin.site.register(Note)
