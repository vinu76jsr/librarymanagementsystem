from django.contrib.auth.models import User
from django.db import models
from datetime import datetime

# Create your models here.
#


class Author(models.Model):
    name = models.CharField(max_length=400)

    def __str__(self):
        return self.name


class Book(models.Model):
    assigned_to = models.ForeignKey(User, blank=True, null=True, related_name='assigned_to_user')
    owned_by = models.ForeignKey(User, null=True, related_name='owned_by_user')
    name = models.CharField(max_length=400)
    author = models.CharField(max_length=400)
    author_model = models.ManyToManyField(Author, null=True, blank=True)
    assigned_on = models.DateTimeField(null=True, blank=True)
    due_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ["-name"]

    def __str__(self):              # __unicode__ on Python 2
        return self.name

    def assigned_to_user(self, user, due_on):
        self.assigned_to = user
        self.assigned_on = datetime.now()
        self.due_on = self.due_on
        self.save()

    def author_name(self):
        author_name = ''
        if self.author:
            author_name = self.author
        elif self.author_model:
            author_name = ','.join(map(str, self.author_model.all()))
        return author_name

    def is_available(self):
        return not bool(self.assigned_to)

    def return_book(self, user):
        self.assigned_to = None
        self.assigned_on = False
        self.save()


class RequestBook(models.Model):
    user = models.ForeignKey(User)
    requested_on = models.DateTimeField(auto_now=True)
    book = models.ForeignKey(Book)