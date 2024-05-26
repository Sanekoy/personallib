from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from library.models import Collection, Book, Author, Publisher, Genre, Tag, Photo
from library.forms import BookForm, AuthorForm, PublisherForm, GenreForm, TagForm
from django.http import HttpRequest
from django.http import QueryDict
from django.http import HttpResponseNotFound
from django.contrib.auth.models import User
from unittest.mock import patch, MagicMock
from library.views import view_collection

class LibraryViewsTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.collection = Collection.objects.create(name="Test Collection")
        self.collection_id = self.collection.id
        self.add_author_url = reverse('add_author') + f'?collection_id={self.collection_id}'
        self.add_book_url = reverse('add_book', kwargs={'collection_id': self.collection_id})
        self.existing_author = Author.objects.create(name='Existing Author')
        self.add_publisher_url = reverse('add_publisher') + f'?collection_id={self.collection_id}'
        self.add_genre_url = reverse('add_genre') + f'?collection_id={self.collection_id}'
        self.add_tag_url = reverse('add_tag') + f'?collection_id={self.collection_id}'

    def test_choose_collection(self):
        response = self.client.get(reverse('choose_collection'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'choose_collection.html')

        # Test POST request
        response = self.client.post(reverse('choose_collection'), {'collection_name': 'New Collection'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('choose_collection'))
        self.assertTrue(Collection.objects.filter(name='New Collection').exists())

    def test_view_collection(self):
        response = self.client.get(reverse('view_collection', kwargs={'collection_id': self.collection_id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'collection.html')
        self.assertEqual(response.context['collection'].id, self.collection_id)

    def test_view_book(self):
        book = Book.objects.create(title="Test Book")
        book.collections.add(self.collection)
        response = self.client.get(reverse('view_book', kwargs={'book_id': book.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book.html')
        self.assertEqual(response.context['book'].id, book.id)

    def test_add_author_get(self):
        response = self.client.get(self.add_author_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_author.html')
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], AuthorForm)
        self.assertEqual(response.context['collection_id'], str(self.collection_id))

    def test_add_author_post_new(self):
        response = self.client.post(self.add_author_url, {
            'name': 'New Author',
            'collection_id': self.collection_id
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.add_book_url)
        self.assertTrue(Author.objects.filter(name='New Author').exists())

    def test_add_author_post_existing(self):
        response = self.client.post(self.add_author_url, {
            'name': 'Existing Author',
            'collection_id': self.collection_id
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_author.html')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Ошибка в форме. Проверьте введенные данные.')

    def test_add_author_post_invalid_form(self):
        response = self.client.post(self.add_author_url, {
            'name': '',
            'collection_id': self.collection_id
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_author.html')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Ошибка в форме. Проверьте введенные данные.')
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], AuthorForm)
        self.assertTrue(response.context['form'].errors)

    def test_add_book_get(self):
        response = self.client.get(self.add_book_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_book.html')
        self.assertIn('book_form', response.context)
        self.assertIsInstance(response.context['book_form'], BookForm)

    def test_add_book_get(self):
        response = self.client.get(self.add_book_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_book.html')
        self.assertIn('book_form', response.context)
        self.assertIsInstance(response.context['book_form'], BookForm)

    def test_add_book_post(self):
        response = self.client.post(self.add_book_url, {
            'title': 'New Book',
            'authors': [self.existing_author.id],
            'collection_id': self.collection_id
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('view_collection', kwargs={'collection_id': self.collection_id}))
        self.assertTrue(Book.objects.filter(title='New Book').exists())

    def test_add_publisher_get(self):
        response = self.client.get(self.add_publisher_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_publisher.html')
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], PublisherForm)

    def test_add_publisher_post_new(self):
        response = self.client.post(self.add_publisher_url, {
            'name': 'New Publisher',
            'collection_id': self.collection_id
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.add_book_url)
        self.assertTrue(Publisher.objects.filter(name='New Publisher').exists())

    def test_add_publisher_post_existing(self):
        Publisher.objects.create(name='Existing Publisher')
        response = self.client.post(self.add_publisher_url, {
            'name': 'Existing Publisher',
            'collection_id': self.collection_id
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_publisher.html')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Ошибка в форме. Проверьте введенные данные.')

    def test_add_genre_get(self):
        response = self.client.get(self.add_genre_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_genre.html')
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], GenreForm)

    def test_add_genre_post_new(self):
        response = self.client.post(self.add_genre_url, {
            'name': 'New Genre',
            'collection_id': self.collection_id
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.add_book_url)
        self.assertTrue(Genre.objects.filter(name='New Genre').exists())

    def test_add_genre_post_existing(self):
        Genre.objects.create(name='Existing Genre')
        response = self.client.post(self.add_genre_url, {
            'name': 'Existing Genre',
            'collection_id': self.collection_id
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_genre.html')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Ошибка в форме. Проверьте введенные данные.')

    def test_add_tag_get(self):
        response = self.client.get(self.add_tag_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_tag.html')
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], TagForm)

    def test_add_tag_post_new(self):
        response = self.client.post(self.add_tag_url, {
            'name': 'New Tag',
            'collection_id': self.collection_id
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.add_book_url)
        self.assertTrue(Tag.objects.filter(name='New Tag').exists())

    def test_add_tag_post_existing(self):
        Tag.objects.create(name='Existing Tag')
        response = self.client.post(self.add_tag_url, {
            'name': 'Existing Tag',
            'collection_id': self.collection_id
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_tag.html')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Ошибка в форме. Проверьте введенные данные.')

class ViewCollectionTestCase(TestCase):
    def setUp(self):
        # Создание объектов для тестов
        self.collection = Collection.objects.create(name='Test Collection')
        self.author = Author.objects.create(name='Test Author')
        self.publisher = Publisher.objects.create(name='Test Publisher')
        self.genre = Genre.objects.create(name='Test Genre')
        self.tag = Tag.objects.create(name='Test Tag')
        self.book = Book.objects.create(title='Test Book', edition_number=1)
        self.book.authors.add(self.author)
        self.book.publishers.add(self.publisher)
        self.book.genres.add(self.genre)
        self.book.tags.add(self.tag)
        self.collection.books.add(self.book)

    def test_view_collection(self):
        url = reverse('view_collection', kwargs={'collection_id': self.collection.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'collection.html')
        self.assertContains(response, 'Test Collection')
        self.assertContains(response, 'Test Book')

    def test_view_collection_with_filter(self):
        url = reverse('view_collection', kwargs={'collection_id': self.collection.id})
        url += '?author={}&publisher={}&genre={}&tag={}'.format(self.author.id, self.publisher.id, self.genre.id, self.tag.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'collection.html')
        self.assertContains(response, 'Test Collection')
        self.assertContains(response, 'Test Book')