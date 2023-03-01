'''Form for book app'''
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from django import forms
from .models import Book, Chapter

class BookForm(forms.ModelForm):
    class Meta:
        model = Book

        fields = [
            'title',
        ]

    title = forms.CharField(widget=forms.TextInput())

class ChapterForm(forms.ModelForm):
    class Meta:
        model = Chapter

        fields = [
            'book',
            'chapter_no',
            'title',
            'content',
        ]
    chapter_no = forms.CharField(widget=forms.TextInput())
    title = forms.CharField(widget=forms.TextInput())
