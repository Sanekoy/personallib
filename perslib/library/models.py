from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator

class Collection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=255)
    edition_number = models.IntegerField(validators=[MaxValueValidator(9999)], blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    authors = models.ManyToManyField('Author', related_name='books')
    publishers = models.ManyToManyField('Publisher', related_name='books')
    genres = models.ManyToManyField('Genre', related_name='books')
    tags = models.ManyToManyField('Tag', related_name='books')
    collections = models.ManyToManyField(Collection, related_name='books')

    def __str__(self):
        return self.title

class Author(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Publisher(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Photo(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='book_photos/')

    def __str__(self):
        return self.image.name