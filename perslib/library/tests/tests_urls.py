from django.urls import reverse, resolve
from library.views import choose_collection, view_collection, view_book, add_author, add_book
from django.test import TestCase

class TestUrls(TestCase):

    def test_choose_collection_url_is_resolved(self):
        url = reverse('choose_collection')
        self.assertEqual(resolve(url).func, choose_collection)

    def test_view_collection_url_is_resolved(self):
        url = reverse('view_collection', args=[1])
        self.assertEqual(resolve(url).func, view_collection)

    def test_view_book_url_is_resolved(self):
        url = reverse('view_book', args=[1])
        self.assertEqual(resolve(url).func, view_book)

    def test_add_author_url_is_resolved(self):
        url = reverse('add_author')
        self.assertEqual(resolve(url).func, add_author)

    def test_add_book_url_is_resolved(self):
        url = reverse('add_book', args=[1])
        self.assertEqual(resolve(url).func, add_book)