'''view for article app'''
import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404

from sudachipy import tokenizer
from sudachipy import dictionary

from .forms import ChapterForm, BookForm
from .models import Book, Chapter, Favourite, Note
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

@login_required
def create_book(request):
    if request.method == "POST":
        title = request.POST['title']
        author = request.POST['author']
        Book.objects.get_or_create(title=title, author=author, user=request.user)
        return redirect("home:home")


@login_required
def details_book(request, id):
    '''rendering home view'''
    book = Book.objects.filter(id=id)[0]
    chapter_list = book.chapters.all()
    context = {
        'book':book,
        'chapter_list':chapter_list
    }
    return render(request, "book/book_details.html", context=context)



class ChapterCreate(LoginRequiredMixin, CreateView):
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
        return redirect("book:chapter_details", pk=self.object.id)

def sorting(lst):
    lst2 = sorted(lst, key=len, reverse=True)
    return lst2   

class ChapterDetails(LoginRequiredMixin, DetailView):
    model = Chapter
    template_name = 'book/chapter_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        favourite_word_list = []
        # meaning_list = []
        for favourite in self.object.favourites.all():
            favourite_word_list.append(favourite.get_str())
            # meaning_list.append(favourite.meaning)
        note_list = []
        for note in self.object.notes.all():
            note_list.append(note.title)
        # print(favourite_word_list)
        # print(meaning_list)
        context["note_list"] = sorting(note_list)
        context["favourite_word_list"] = sorting(favourite_word_list)
        # context["meaning_list"] = meaning_list

        return context

    def get_template_names(self):
        return self.template_name

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data()
        # print(context)
        template_name = self.get_template_names()
        return render(request, template_name, context)


@login_required
def add_favourite_word(request):
    if request.method == "POST":
        data = json.load(request)
        document_id = data["document_id"]
        chapter = Chapter.objects.get(id=document_id)
        word = data["word"]
        no = data["no"]
        Favourite.objects.get_or_create(chapter=chapter, word=word, no=no)
        return JsonResponse({"success": True}, status=200)
    

@login_required
def remove_from_favourite_word(request):
    if request.method == "POST":
        data = json.load(request)
        chapter = Chapter.objects.get(id=data['document_id'])
        word = data['word']
        no = data['no']
        Favourite.objects.filter(chapter=chapter, word=word, no=no).delete()
        return JsonResponse({"success": True}, status=200)
    return JsonResponse({"success": False}, status=400)
    

@login_required
def create_note(request):
    if request.method == "POST":
        data = json.load(request)
        document_id = data["document_id"]
        chapter = Chapter.objects.get(id=document_id)
        word = data['word']
        content = data['content']
        Note.objects.get_or_create(chapter=chapter, title=word, content=content)
        return JsonResponse({"success": True}, status=200)

@login_required
def get_note(request):
    if request.method == "POST":
        context = {}
        data = json.load(request)
        chapter = Chapter.objects.get(id=data['document_id'])
        word = data['word']
        note = Note.objects.filter(chapter=chapter, title=word)
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
        chapter = Chapter.objects.get(id=data['document_id'])
        word = data['word']
        Note.objects.filter(chapter=chapter, title=word).delete()
        return JsonResponse({"success": True}, status=200)
    return JsonResponse({"success": False}, status=400)
