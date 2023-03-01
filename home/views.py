from django.shortcuts import render

from article.models import Article
from book.models import Book

# Create your views here.

def home(request):
    '''rendering home view'''
    article_list = Article.objects.all()
    book_list = Book.objects.all()
    context = {
        'article_list':article_list,
        'book_list':book_list
    }
    return render(request, "home/index.html", context=context)
