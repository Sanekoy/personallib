from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Collection, Book, Author, Publisher, Genre, Tag
from .forms import BookForm

def choose_collection(request):
    if request.method == 'POST':
        collection_name = request.POST['collection_name']
        Collection.objects.create(name=collection_name)
        return redirect('choose_collection') 
    else:
        collections = Collection.objects.all()
        return render(request, 'choose_collection.html', {'collections': collections})
    
def view_collection(request, collection_id):
    collection = get_object_or_404(Collection, pk=collection_id)
    books = collection.books.all()

    query = request.GET.get('q')
    author_id = request.GET.get('author')
    publisher_id = request.GET.get('publisher')
    genre_id = request.GET.get('genre')
    tag_id = request.GET.get('tag')

    if query:
        books = books.filter(title__icontains=query)

    if author_id:
        books = books.filter(authors__id=author_id)

    if publisher_id:
        books = books.filter(publishers__id=publisher_id)

    if genre_id:
        books = books.filter(genres__id=genre_id)

    if tag_id:
        books = books.filter(tags__id=tag_id)

    all_books = Book.objects.exclude(collections=collection)
    all_authors = Author.objects.all()
    all_publishers = Publisher.objects.all()
    all_genres = Genre.objects.all()
    all_tags = Tag.objects.all()

    return render(request, 'collection.html', {
        'collection': collection, 
        'books': books, 
        'all_books': all_books,
        'all_authors': all_authors,
        'all_publishers': all_publishers,
        'all_genres': all_genres,
        'all_tags': all_tags,
    })

def add_book(request, collection_id):
    collection = get_object_or_404(Collection, id=collection_id)
    all_books = Book.objects.all()
    all_authors = Author.objects.all()
    all_publishers = Publisher.objects.all()
    all_genres = Genre.objects.all()
    all_tags = Tag.objects.all()
    all_collections = Collection.objects.all()

    if request.method == "POST":
        if 'new_book' in request.POST:
            # Обработайте данные из HTML-формы
            title = request.POST.get('title')
            edition_number = request.POST.get('edition_number')
            comment = request.POST.get('comment')
            authors = request.POST.getlist('authors')
            publishers = request.POST.getlist('publishers')
            genres = request.POST.getlist('genres')
            tags = request.POST.getlist('tags')
            collections = request.POST.getlist('collections')

            # Создайте новую книгу и сохраните ее в базе данных
            new_book = Book.objects.create(title=title, edition_number=edition_number, comment=comment)
            new_book.authors.set(authors)
            new_book.publishers.set(publishers)
            new_book.genres.set(genres)
            new_book.tags.set(tags)
            new_book.collections.set(collections)

            collection.books.add(new_book)
            return redirect('collection_detail', pk=collection.id)
        else:
            book_id = request.POST.get('book_id')
            book = get_object_or_404(Book, id=book_id)
            collection.books.add(book)
            return redirect('collection_detail', pk=collection.id)

    context = {
        'collection': collection,
        'all_books': all_books,
        'all_authors': all_authors,
        'all_publishers': all_publishers,
        'all_genres': all_genres,
        'all_tags': all_tags,
        'all_collections': all_collections,
    }
    return render(request, 'add_book.html', context)

def view_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'book.html', {'book': book})