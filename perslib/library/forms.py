from django import forms
from .models import Book, Author, Publisher, Genre, Tag
from django.utils.translation import gettext_lazy as _

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'edition_number', 'comment']
        labels = {
            'title': 'Название',
            'edition_number': 'Номер издания',
            'comment': 'Комментарий',
        }
    def clean_edition_number(self):
        edition_number = self.cleaned_data.get('edition_number')
        if edition_number is not None:
            if edition_number > 9999:
                raise forms.ValidationError("Номер издания не должен превышать 9999.")
        return edition_number

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name']
        labels = {
            'name': 'Имя автора',
        }
    def clean_name(self):
        name = self.cleaned_data['name']
        if Author.objects.filter(name=name).exists():
            raise forms.ValidationError(_('Такой автор уже существует!'))
        return name

class PublisherForm(forms.ModelForm):
    class Meta:
        model = Publisher
        fields = ['name']
        labels = {
            'name': 'Название издателя',
        }
    def clean_name(self):
        name = self.cleaned_data['name']
        if Publisher.objects.filter(name=name).exists():
            raise forms.ValidationError(_('Такой издатель уже существует!'))
        return name        
        

class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['name']
        labels = {
            'name': 'Название жанра',
        }
    def clean_name(self):
        name = self.cleaned_data['name']
        if Genre.objects.filter(name=name).exists():
            raise forms.ValidationError(_('Такой жанр уже существует!'))
        return name      

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']
        labels = {
            'name': 'Метка',
        }
    def clean_name(self):
        name = self.cleaned_data['name']
        if Tag.objects.filter(name=name).exists():
            raise forms.ValidationError(_('Такая метка уже существует!'))
        return name      
        
