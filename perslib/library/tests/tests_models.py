from django.test import TestCase
from library.models import Collection, Book, Author, Publisher, Genre, Tag, Photo


class CollectionModelTest(TestCase):

    def test_collection_creation(self):
        collection = Collection.objects.create(name="Test Collection")
        self.assertEqual(collection.name, "Test Collection")

    def test_collection_str(self):
        collection = Collection.objects.create(name="Test Collection")
        self.assertEqual(str(collection), "Test Collection")

        # Create a Book instance with all fields properly set
    def test_create_book_with_all_fields(self):
        from django.contrib.auth.models import User
        from library.models import Book, Author, Publisher, Genre, Tag, Collection
        author = Author.objects.create(name="John Doe")
        publisher = Publisher.objects.create(name="BigPub")
        genre = Genre.objects.create(name="Fiction")
        tag = Tag.objects.create(name="Bestseller")
        collection = Collection.objects.create(name="My Collection")
        book = Book.objects.create(title="New Book", edition_number=1, comment="Great book")
        book.authors.add(author)
        book.publishers.add(publisher)
        book.genres.add(genre)
        book.tags.add(tag)
        book.collections.add(collection)
        assert book.title == "New Book"
        assert book.edition_number == 1
        assert book.comment == "Great book"
        assert author in book.authors.all()
        assert publisher in book.publishers.all()
        assert genre in book.genres.all()
        assert tag in book.tags.all()
        assert collection in book.collections.all()

class BookModelTest(TestCase):

    def setUp(self):
        self.collection = Collection.objects.create(name="Test Collection")

    def test_book_creation(self):
        book = Book.objects.create(title="Test Book")
        book.collections.add(self.collection)
        self.assertEqual(book.title, "Test Book")
        self.assertEqual(book.collections.first(), self.collection)

    def test_book_str(self):
        book = Book.objects.create(title="Test Book")
        self.assertEqual(str(book), "Test Book")

    # Add more tests for relationships and other fields as needed

# Add similar tests for Author, Publisher, Genre, Tag, and Photo models