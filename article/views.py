'''view for article app'''
import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required

from .forms import ArticleForm
from .models import Article, Favourite

class ArticleCreate(CreateView):
    form_class = ArticleForm
    template_name = 'article/article_create.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return redirect("home:home")

class ArticleView(DetailView):
    model = Article
    template_name = 'article/article_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        favourite_word_list = []
        meaning_list = []
        for favourite in self.object.favourites.all():
            favourite_word_list.append(favourite.word)
            meaning_list.append(favourite.meaning)
        # print(favourite_word_list)
        # print(meaning_list)
        context["favourite_word_list"] = favourite_word_list
        context["meaning_list"] = meaning_list

        return context

    def get_template_names(self):
        return self.template_name

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data()
        template_name = self.get_template_names()
        return render(request, template_name, context)


# @login_required

def add_favourite_word(request):
    if request.method == "POST":
        data = json.load(request)
        article_id = data["article_id"]
        article = Article.objects.get(id=article_id)
        selected_word = data["selected_word"]
        meaning = data["meaning"]
        Favourite.objects.get_or_create(article=article, word=selected_word, meaning=meaning)

        return JsonResponse({"success": True}, status=200)
