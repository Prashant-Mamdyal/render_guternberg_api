from rest_framework import serializers
from .models import Book, Author, Bookshelf, Language, Subject, Format

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['name', 'birth_year', 'death_year']

class BookshelfSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookshelf
        fields = ['name']

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['code']

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['name']

class FormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Format
        fields = ['mime_type', 'url']        

class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True, read_only=True)
    bookshelves = BookshelfSerializer(many=True, read_only=True)
    languages = LanguageSerializer(many=True, read_only=True)
    subjects = SubjectSerializer(many=True, read_only=True)
    formats = FormatSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'download_count', 'authors', 'bookshelves', 'languages', 'subjects', 'formats']