from django.contrib import admin
from .models import Author, Book, Bookshelf, Language, Subject, Format

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Bookshelf)
admin.site.register(Language)
admin.site.register(Subject)
admin.site.register(Format)