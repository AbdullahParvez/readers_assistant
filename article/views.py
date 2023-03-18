'''view for article app'''
import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic.edit import CreateView
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import ArticleForm
from .models import Article, Favourite, Note


class ArticleCreate(LoginRequiredMixin, CreateView):
    form_class = ArticleForm
    template_name = 'article/article_create.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return redirect("home:home")
    
def sorting(lst):
    lst2 = sorted(lst, key=len, reverse=True)
    return lst2   

class ArticleView(LoginRequiredMixin, DetailView):
    model = Article
    template_name = 'article/article_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        favourite_word_list = []
        for favourite in self.object.favourites.all():
            favourite_word_list.append(favourite.get_str())
        note_list = []
        for note in self.object.notes.all():
            note_list.append(note.title)
        context["note_list"] = sorting(note_list)
        context["favourite_word_list"] = sorting(favourite_word_list)

        return context

    def get_template_names(self):
        return self.template_name

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data()
        template_name = self.get_template_names()
        return render(request, template_name, context)


@login_required
def add_favourite_word(request):
    if request.method == "POST":
        data = json.load(request)
        article_id = data["article_id"]
        article = Article.objects.get(id=article_id)
        word = data["word"]
        no = data["no"]
        Favourite.objects.get_or_create(article=article, word=word, no=no)

        return JsonResponse({"success": True}, status=200)


@login_required
def remove_from_favourite_word(request):
    if request.method == "POST":
        data = json.load(request)
        article = Article.objects.get(id=data['article_id'])
        word = data['word']
        no = data['no']
        Favourite.objects.filter(article=article, word=word, no=no).delete()
        return JsonResponse({"success": True}, status=200)
    return JsonResponse({"success": False}, status=400)


@login_required
def create_note(request):
    if request.method == "POST":
        data = json.load(request)
        article_id = data["article_id"]
        article = Article.objects.get(id=article_id)
        word = data['word']
        content = data['content']
        Note.objects.get_or_create(article=article, title=word, content=content)
        return JsonResponse({"success": True}, status=200)
    return JsonResponse({"success": False}, status=400)


def get_note(request):
    if request.method == "POST":
        context = {}
        data = json.load(request)
        # print(data['word'])
        article = Article.objects.get(id=data['article_id'])
        word = data['word']
        # print(article, word)
        note = Note.objects.filter(article=article, title=word)
        # print(note.content)
        if note:
            context['content'] = note[0].content
        else:
            context['content'] = ''
        return JsonResponse({"success": True, 'context': context}, status=200)
    return JsonResponse({"success": False}, status=400)


@login_required
def delete_note(request):
    if request.method == "POST":
        data = json.load(request)
        article = Article.objects.get(id=data['article_id'])
        word = data['word']
        Note.objects.filter(article=article, title=word).delete()
        return JsonResponse({"success": True}, status=200)
    return JsonResponse({"success": False}, status=400)