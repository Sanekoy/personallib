from django.contrib import admin
from .models import Collection, Book, Author, Publisher, Genre, Tag, Photo 

admin.site.register(Collection)
admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Publisher)
admin.site.register(Genre)
admin.site.register(Tag)
admin.site.register(Photo)