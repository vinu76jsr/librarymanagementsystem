from django.contrib import admin

# Register your models here.
from mainapp.models import Book, Author, RequestBook


class BookAdmin(admin.ModelAdmin):

    fields = ['author', 'name']

class AuthorAdmin(admin.ModelAdmin):
    pass

class RequestAdmin(admin.ModelAdmin):
    pass

admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(RequestBook, RequestAdmin)
