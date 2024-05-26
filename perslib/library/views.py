from django.shortcuts import render, redirect, get_object_or_404
from .models import Collection, Book, Author, Publisher, Genre, Tag, Photo
from .forms import BookForm, AuthorForm, PublisherForm, GenreForm, TagForm, PhotoForm
from django.urls import reverse
from django.contrib import messages
from django.db import IntegrityError

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

def view_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    collection = get_object_or_404(Collection, pk=collection_id)
    return render(request, 'book.html', {'book': book, 'collection': collection})

def delete_book(request, collection_id, book_id):
    collection = get_object_or_404(Collection, pk=collection_id)
    book = get_object_or_404(Book, pk=book_id)

    # Удаление связи между книгой и коллекцией
    book.collections.remove(collection)

    # Проверка, есть ли еще коллекции, связанные с книгой
    if not book.collections.exists():
        # Если нет, удаляем книгу полностью
        book.delete()
        messages.success(request, 'Книга успешно удалена.')
    else:
        messages.success(request, 'Книга успешно удалена из коллекции.')

    return redirect('view_collection', collection_id=collection_id)

def edit_book(request, collection_id, book_id):
    collection = get_object_or_404(Collection, pk=collection_id)
    book = get_object_or_404(Book, pk=book_id)

    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Книга успешно обновлена.')
            return redirect('view_book', collection_id=collection_id, book_id=book_id)
    else:
        form = BookForm(instance=book)

    return render(request, 'edit_book.html', {'book': book, 'collection': collection, 'form': form})

def add_book(request, collection_id):
    collection = get_object_or_404(Collection, id=collection_id)

    if request.method == "POST":
        book_form = BookForm(request.POST, request.FILES)
        author_form = AuthorForm(request.POST)
        publisher_form = PublisherForm(request.POST)
        genre_form = GenreForm(request.POST)
        tag_form = TagForm(request.POST)

        if book_form.is_valid():
            book = book_form.save(commit=False)
            book.save()

            photos = request.FILES.getlist('photos')
            for photo in photos:
                Photo.objects.create(book=book, image=photo)

            collection.books.add(book)

            # Обработка авторов
            for author_id in request.POST.getlist('authors'):
                try:
                    author = Author.objects.get(id=author_id)
                    book.authors.add(author)
                except Author.DoesNotExist:
                    pass

            # Обработка издателей
            for publisher_id in request.POST.getlist('publishers'):
                try:
                    publisher = Publisher.objects.get(id=publisher_id)
                    book.publishers.add(publisher)
                except Publisher.DoesNotExist:
                    pass

            # Обработка жанров
            for genre_id in request.POST.getlist('genres'):
                try:
                    genre = Genre.objects.get(id=genre_id)
                    book.genres.add(genre)
                except Genre.DoesNotExist:
                    pass

            # Обработка тегов
            for tag_id in request.POST.getlist('tags'):
                try:
                    tag = Tag.objects.get(id=tag_id)
                    book.tags.add(tag)
                except Tag.DoesNotExist:
                    pass

            return redirect('view_collection', collection_id=collection.id)

    else:
        initial_data = {
            'title': request.GET.get('title'),
            'edition_number': request.GET.get('edition_number'),
            'comment': request.GET.get('comment'),
        }
        book_form = BookForm(initial=initial_data)
        author_form = AuthorForm()
        publisher_form = PublisherForm()
        genre_form = GenreForm()
        tag_form = TagForm()

        context = {
            'collection': collection,
            'book_form': book_form,
            'author_form': author_form,
            'publisher_form': publisher_form,
            'genre_form': genre_form,
            'tag_form': tag_form,
            'all_authors': Author.objects.all(),
            'all_publishers': Publisher.objects.all(),
            'all_genres': Genre.objects.all(),
            'all_tags': Tag.objects.all(),
        }
        return render(request, 'add_book.html', context)

def add_author(request):
    collection_id = request.GET.get('collection_id')  # Получаем collection_id из GET-параметров
    
    if request.method == "POST":
        form = AuthorForm(request.POST)
        collection_id = request.POST.get('collection_id')  # Получаем collection_id из POST-параметров
        if form.is_valid():
            try:
                form.save()
                if collection_id:
                    return redirect(reverse('add_book', kwargs={'collection_id': collection_id}))
                else:
                    return redirect('choose_collection')  # Например, перенаправляем на выбор коллекции 
            except IntegrityError:
                messages.error(request, 'Автор с таким именем уже существует!')
        else:
            messages.error(request, 'Ошибка в форме. Проверьте введенные данные.')
    
    else:
        form = AuthorForm()

    return render(request, 'add_author.html', {'form': form, 'collection_id': collection_id})


def add_publisher(request, collection_id=None):
    collection_id = request.GET.get('collection_id')
    if request.method == "POST":
        form = PublisherForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                collection_id = request.POST.get('collection_id')  # Получаем collection_id из GET-параметров

                if collection_id:
                    return redirect(reverse('add_book', kwargs={'collection_id': collection_id}))
                else:
                    return redirect('choose_collection')  # Например, перенаправляем на выбор коллекции 
            except IntegrityError:
                messages.error(request, 'Такой издатель уже существует!')
        else:
            messages.error(request, 'Ошибка в форме. Проверьте введенные данные.')
    else:
        form = PublisherForm()
    return render(request, 'add_publisher.html', {'form': form})

def add_genre(request, collection_id=None):
    collection_id = request.GET.get('collection_id')
    if request.method == "POST":
        form = GenreForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                collection_id = request.POST.get('collection_id')  # Получаем collection_id из GET-параметров

                if collection_id:
                    return redirect(reverse('add_book', kwargs={'collection_id': collection_id}))
                else:
                    return redirect('choose_collection')  # Например, перенаправляем на выбор коллекции 
            except IntegrityError:
                messages.error(request, 'Такой жанр уже существует!')
        else:
            messages.error(request, 'Ошибка в форме. Проверьте введенные данные.')
    else:
        form = GenreForm()
    return render(request, 'add_genre.html', {'form': form})

def add_tag(request, collection_id=None):
    collection_id = request.GET.get('collection_id')
    if request.method == "POST":
        form = TagForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                collection_id = request.POST.get('collection_id')  # Получаем collection_id из GET-параметров

                if collection_id:
                    return redirect(reverse('add_book', kwargs={'collection_id': collection_id}))
                else:
                    return redirect('choose_collection')  # Например, перенаправляем на выбор коллекции 
            except IntegrityError:
                messages.error(request, 'Такая метка уже существует!')
        else:
            messages.error(request, 'Ошибка в форме. Проверьте введенные данные.')
    else:
        form = TagForm()
    return render(request, 'add_tag.html', {'form': form})