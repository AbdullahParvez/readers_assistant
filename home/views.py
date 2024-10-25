from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from article.models import Article
from book.models import Book

# Create your views here.


def home(request):
    '''rendering home view'''
    article_list = Article.objects.filter(is_public=True)
    context = {
        'article_list':article_list,
    }
    return render(request, "home/home.html", context=context)

@login_required
def index(request):
    '''rendering home view'''
    article_list = request.user.articles.all()
    book_list = request.user.books.all()
    context = {
        'article_list':article_list,
        'book_list':book_list
    }
    return render(request, "home/index.html", context=context)


def policy(request):
    '''rendering home view'''
    return render(request, "home/privacy_policy.html")
