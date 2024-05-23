from django import forms
from .models import Book, Author, Publisher, Genre, Tag

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'edition_number', 'comment']

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name']

class PublisherForm(forms.ModelForm):
    class Meta:
        model = Publisher
        fields = ['name']

class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['name']

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']