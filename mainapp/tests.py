import unittest
from django.contrib.auth.models import User
from datetime import date

# Create your tests here.
from mainapp.models import Book


class BookReleaseTestCase(unittest.TestCase):

    def setUp(self):
        self.user = User.objects.create_user('admin', 'admin@test.com', 'pass')
        self.random_user = User.objects.create_user('random', 'random@test.com', 'pass')
        self.book = Book.objects.create(assigned_to=self.user,
                                        name='Test Book',
                                        author='Test Author',
                                        assigned_on=date.today())

    def tearDown(self):
        User.objects.all().delete()
        Book.objects.all().delete()

    def test_book_release(self):
        with self.assertRaises(AssertionError):
            self.book.return_book(self.random_user)
        self.book.assigned_to = self.user
        self.book.save()
        self.book.return_book(self.user)
        self.book = Book.objects.get(id=self.book.id)
        self.assertIsNone(self.book.assigned_to)


