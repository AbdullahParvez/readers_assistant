'''view for article app'''
import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from sudachipy import tokenizer
from sudachipy import dictionary

from .forms import ChapterForm, BookForm
from .models import Book, Chapter, Favourite
from jmdict.models import Dictionary_Entry, Sense, Example

from mongoengine import *

connect('jmdict')
tokenizer_obj = dictionary.Dictionary(dict_type='core').create()
mode = tokenizer.Tokenizer.SplitMode.A


# class BookCreate(CreateView):
#     form_class = BookForm
#     template_name = 'book/book_create.html'
#     def form_valid(self, form):
#         self.object = form.save(commit=False)
#         self.object.save()
#         return redirect("home:home")

def create_book(request):
    if request.method == "POST":
        title = request.POST['title']
        Book.objects.get_or_create(title=title)
        return redirect("home:home")


def details_book(request, id):
    '''rendering home view'''
    book = Book.objects.filter(id=id)[0]
    chapter_list = book.chapters.all()
    context = {
        'book':book,
        'chapter_list':chapter_list
    }
    return render(request, "book/book_details.html", context=context)



class ChapterCreate(CreateView):
    form_class = ChapterForm
    template_name = 'book/chapter_create.html'

    def get_initial(self):
        book = get_object_or_404(Book, id=self.kwargs.get('book_id'))
        return {
            'book':book,
        }

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return redirect("home:home")

class ChapterDetails(DetailView):
    model = Chapter
    template_name = 'book/chapter_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # chapter = self.get_queryset()
        # print(chapter)
        favourite_word_list = []
        meaning_list = []
        for favourite in self.object.book.favourites.all():
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
        # print(context)
        template_name = self.get_template_names()
        return render(request, template_name, context)



def add_favourite_word(request):
    if request.method == "POST":
        data = json.load(request)
        book_id = data["book_id"]
        book = Book.objects.get(id=book_id)
        selected_word = data["selected_word"]
        meaning = data["meaning"]
        Favourite.objects.get_or_create(book=book, word=selected_word, meaning=meaning)

        return JsonResponse({"success": True}, status=200)
