from django.contrib import admin
from .models import Collection, Book, Author, Publisher, Genre, Tag, Photo

class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 1
    fields = ('image',)

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_authors', 'get_publishers', 'get_genres', 'edition_number',)
    #list_filter = ('authors', 'publishers', 'genres', 'tags')
    search_fields = ('title', 'authors__name', 'publishers__name')
    #filter_horizontal = ('authors', 'publishers', 'genres', 'tags', 'collections')
    inlines = [PhotoInline]

    def get_authors(self, obj):
        return ", ".join([author.name for author in obj.authors.all()])
    get_authors.short_description = 'Authors'

    def get_publishers(self, obj):
        return ", ".join([publisher.name for publisher in obj.publishers.all()])
    get_publishers.short_description = 'Publishers'

    def get_genres(self, obj):
        return ", ".join([genre.name for genre in obj.genres.all()])
    get_genres.short_description = 'Genres'

class AuthorAdmin(admin.ModelAdmin):
    search_fields = ('name',)

class PublisherAdmin(admin.ModelAdmin):
    search_fields = ('name',)

class GenreAdmin(admin.ModelAdmin):
    search_fields = ('name',)

class TagAdmin(admin.ModelAdmin):
    search_fields = ('name',)

class CollectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_book_count')
    search_fields = ('name',)

    def get_book_count(self, obj):
        return obj.books.count()
    get_book_count.short_description = 'Number of Books'

admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Publisher, PublisherAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Collection, CollectionAdmin)
admin.site.register(Photo)