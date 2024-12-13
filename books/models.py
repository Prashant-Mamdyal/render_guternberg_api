from django.db import models


class Author(models.Model):
    birth_year = models.SmallIntegerField(null=True, blank=True)
    death_year = models.SmallIntegerField(null=True, blank=True)
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Book(models.Model):
    download_count = models.IntegerField(null=True, blank=True)
    gutenberg_id = models.IntegerField(unique=True)
    media_type = models.CharField(max_length=16)
    title = models.CharField(max_length=1024, null=True, blank=True)
    authors = models.ManyToManyField('Author', related_name='books')
    bookshelves = models.ManyToManyField('Bookshelf', related_name='books')
    languages = models.ManyToManyField('Language', related_name='books')
    subjects = models.ManyToManyField('Subject', related_name='books')

    def __str__(self):
        return self.title


class Bookshelf(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class Language(models.Model):
    code = models.CharField(max_length=4, unique=True)

    def __str__(self):
        return self.code


class Subject(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Format(models.Model):
    mime_type = models.CharField(max_length=32)
    url = models.CharField(max_length=256)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='formats')

    def __str__(self):
        return f"{self.mime_type} - {self.url}"
