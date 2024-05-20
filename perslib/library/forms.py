# books/forms.py

from django import forms
from .models import Book, Author, Genre, Publisher, Tag

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'edition_number', 'comment', 'authors', 'publishers', 'genres', 'tags', 'collections']
        widgets = {
            'authors': forms.SelectMultiple(),
            'publishers': forms.SelectMultiple(),
            'genres': forms.SelectMultiple(),
            'tags': forms.SelectMultiple(),
            'collections': forms.SelectMultiple(),
        }