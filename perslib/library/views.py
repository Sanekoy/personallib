from django.shortcuts import render, redirect, get_object_or_404
from .models import Collection, Book, Author, Publisher, Genre, Tag, Photo
from .forms import BookForm, AuthorForm, PublisherForm, GenreForm, TagForm, UserRegistrationForm
from django.contrib.auth import login, authenticate
from django.urls import reverse
from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

@login_required
def choose_collection(request):
    if request.method == 'POST':
        collection_name = request.POST['collection_name']
        Collection.objects.create(name=collection_name, user=request.user)
        return redirect('choose_collection')
    else:
        collections = Collection.objects.filter(user=request.user).order_by('name')
        return render(request, 'choose_collection.html', {'collections': collections})

    
def view_collection(request, collection_id):
    collection = get_object_or_404(Collection, pk=collection_id)
    books = collection.books.all().order_by('title')

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

def view_book(request, collection_id, book_id):
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
    action = request.POST.get('action', '')

    if request.method == 'POST':
        if action.startswith('remove_author_'):
            author_id = int(action.split('_')[-1])
            author = Author.objects.get(pk=author_id)
            book.authors.remove(author)
        elif action == 'add_author':
            author_id = request.POST.get('add_author')
            if author_id:
                author = Author.objects.get(pk=author_id)
                book.authors.add(author)
        elif action.startswith('remove_publisher_'):
            publisher_id = int(action.split('_')[-1])
            publisher = Publisher.objects.get(pk=publisher_id)
            book.publishers.remove(publisher)
        elif action == 'add_publisher':
            publisher_id = request.POST.get('add_publisher')
            if publisher_id:
                publisher = Publisher.objects.get(pk=publisher_id)
                book.publishers.add(publisher)
        elif action.startswith('remove_genre_'):
            genre_id = int(action.split('_')[-1])
            genre = Genre.objects.get(pk=genre_id)
            book.genres.remove(genre)
        elif action == 'add_genre':
            genre_id = request.POST.get('add_genre')
            if genre_id:
                genre = Genre.objects.get(pk=genre_id)
                book.genres.add(genre)
        elif action.startswith('remove_tag_'):
            tag_id = int(action.split('_')[-1])
            tag = Tag.objects.get(pk=tag_id)
            book.tags.remove(tag)
        elif action == 'add_tag':
            tag_id = request.POST.get('add_tag')
            if tag_id:
                tag = Tag.objects.get(pk=tag_id)
                book.tags.add(tag)
        elif action.startswith('remove_photo_'):
            photo_id = int(action.split('_')[-1])
            photo = Photo.objects.get(pk=photo_id)
            photo.delete()  # Удаляем фото
        elif action == 'add_photo':
            if request.FILES.get('add_photo'):
                photo = Photo(book=book, image=request.FILES['add_photo'])
                photo.save()
        elif action == 'save':
            # Обработка основных данных
            book.title = request.POST.get('title')
            book.edition_number = request.POST.get('edition_number') or None
            book.comment = request.POST.get('comment')
            book.save()

            messages.success(request, 'Книга успешно обновлена.')
            return redirect('view_book', collection_id=collection_id, book_id=book_id)

        return redirect('edit_book', collection_id=collection_id, book_id=book_id)

    else:
        available_authors = Author.objects.all()
        available_publishers = Publisher.objects.all()
        available_genres = Genre.objects.all()
        available_tags = Tag.objects.all()
        return render(request, 'edit_book.html', {
            'book': book,
            'collection': collection,
            'available_authors': available_authors,
            'available_publishers': available_publishers,
            'available_genres': available_genres,
            'available_tags': available_tags,
        })

def add_book(request, collection_id):
    collection = get_object_or_404(Collection, id=collection_id)
    all_books = Book.objects.all()

    if request.method == "POST":
        # Добавление существующей книги
        if 'book_id' in request.POST:
            book_id = request.POST.get('book_id')
            book = get_object_or_404(Book, id=book_id)
            collection.books.add(book)
            return redirect('view_collection', collection_id=collection.id)

        # Создание новой книги
        elif 'title' in request.POST:
            book_form = BookForm(request.POST, request.FILES)
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

            # Если форма не валидна, отображаем ее снова с ошибками
            initial_data = {
                'title': request.GET.get('title'),
                'edition_number': request.GET.get('edition_number'),
                'comment': request.GET.get('comment'),
            }
            author_form = AuthorForm(request.POST)
            publisher_form = PublisherForm(request.POST)
            genre_form = GenreForm(request.POST)
            tag_form = TagForm(request.POST)

            context = {
                'collection': collection,
                'book_form': book_form,  # Передаем форму с ошибками обратно в контекст
                'author_form': author_form,
                'publisher_form': publisher_form,
                'genre_form': genre_form,
                'tag_form': tag_form,
                'all_authors': Author.objects.all().order_by('name'),
                'all_publishers': Publisher.objects.all().order_by('name'),
                'all_genres': Genre.objects.all().order_by('name'),
                'all_tags': Tag.objects.all().order_by('name'),
                'all_books': all_books,
            }
            return render(request, 'add_book.html', context)

    # Отображение формы (GET-запрос)
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
            'all_books': all_books,
        }
        return render(request, 'add_book.html', context)
    
def add_author(request):
    collection_id = request.GET.get('collection_id') or request.POST.get('collection_id')
    book_id = request.GET.get('book_id') or request.POST.get('book_id')

    if book_id == 'None':
        book_id = None

    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                if book_id:
                    return redirect('edit_book', collection_id=collection_id, book_id=book_id)
                elif collection_id:
                    return redirect('add_book', collection_id=collection_id)
                else:
                    return redirect('choose_collection')
            except IntegrityError:
                pass
    else:
        form = AuthorForm()

    context = {
        'form': form,
        'collection_id': collection_id,
        'book_id': book_id,
    }
    return render(request, 'add_author.html', context)


def add_publisher(request):
    collection_id = request.GET.get('collection_id') or request.POST.get('collection_id')
    book_id = request.GET.get('book_id') or request.POST.get('book_id')

    if book_id == 'None':
        book_id = None

    if request.method == "POST":
        form = PublisherForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                if book_id:
                    return redirect('edit_book', collection_id=collection_id, book_id=book_id)
                elif collection_id:
                    return redirect('add_book', collection_id=collection_id)
                else:
                    return redirect('choose_collection')
            except IntegrityError:
                pass
    else:
        form = PublisherForm()

    context = {
        'form': form,
        'collection_id': collection_id,
        'book_id': book_id,
    }
    return render(request, 'add_publisher.html', context)


def add_genre(request):
    collection_id = request.GET.get('collection_id') or request.POST.get('collection_id')
    book_id = request.GET.get('book_id') or request.POST.get('book_id')

    if book_id == 'None':
        book_id = None

    if request.method == "POST":
        form = GenreForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                if book_id:
                    return redirect('edit_book', collection_id=collection_id, book_id=book_id)
                elif collection_id:
                    return redirect('add_book', collection_id=collection_id)
                else:
                    return redirect('choose_collection')
            except IntegrityError:
                pass
    else:
        form = GenreForm()

    context = {
        'form': form,
        'collection_id': collection_id,
        'book_id': book_id,
    }
    return render(request, 'add_genre.html', context)

def add_tag(request, collection_id=None):
    collection_id = request.GET.get('collection_id') or request.POST.get('collection_id')
    book_id = request.GET.get('book_id') or request.POST.get('book_id')

    if book_id == 'None':
        book_id = None

    if request.method == "POST":
        form = TagForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                if book_id:
                    return redirect('edit_book', collection_id=collection_id, book_id=book_id)
                elif collection_id:
                    return redirect('add_book', collection_id=collection_id)
                else:
                    return redirect('choose_collection')
            except IntegrityError:
                pass
    else:
        form = TagForm()

    context = {
        'form': form,
        'collection_id': collection_id,
        'book_id': book_id,
    }
    return render(request, 'add_tag.html', context)

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('choose_collection')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('choose_collection')
            else:
                return render(request, 'login.html', {'form': form})
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')