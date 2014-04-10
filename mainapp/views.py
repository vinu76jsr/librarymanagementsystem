from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render_to_response
from django.views.generic import ListView, View
from mainapp.models import Book
from datetime import datetime, date


@login_required(login_url='/login/google')
def index(request):
    # full_name = request.user.get_username()
    # response_dict = {
    #     'full_name':full_name,
    #     }
    # book_list = Book.objects.all()
    return HttpResponseRedirect('/books')

from django.contrib.auth import logout


@login_required(login_url='/login/google')
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out')
    return HttpResponseRedirect('/')


@receiver(pre_save, sender=User)
def make_user_staff(sender, **kwargs):
    sender.is_staff = True


def login_error(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    return HttpResponse('login error, perhaps you used wrong account')


class BookListView(ListView, ):

    model = Book

    # def get_context_data(self, **kwargs):
    #     context = super(BookListView, self).get_context_data(**kwargs)
    #     return context


class BookAssignView(View):

    template_name = 'mainapp/book_assign_form.html'

    def get(self, request, *args, **kwargs):
        try:
            book = Book.objects.get(id=kwargs['book_id'])
        except Book.DoesNotExist():
            messages.error(request, 'Specified book does not exist')
            return HttpResponseRedirect('/')
        today = '%s' % date.today()
        return render(request, self.template_name, {'book': book,
                                                    'today': today,
                                                    'user': request.user})

    def post(self, request, *args, **kwargs):
        try:
            book = Book.objects.get(id=kwargs['book_id'])
        except Book.DoesNotExist():
            messages.error(request, 'Specified book does not exist')
            return HttpResponseRedirect('/')
        redirect_url = '/books'
        if book.assigned_to is None:
            book.assigned_to_user(request.user, due_on=request.POST.get('due_date'))
            message = messages.success(request, 'Book is assigned to you and is due on %s' % book.due_on)
        else:
            message = messages.error(request, 'Book already assigned to Somebody else')
        return HttpResponseRedirect(redirect_url, {'message': message})


class BookReleaseView(View):

    template_name = 'mainapp/book_release_form.html'

    def post(self, request, *args, **kwargs):
        try:
            book = Book.objects.get(id=kwargs['book_id'])
        except Book.DoesNotExist():
            messages.error(request, 'Specified book does not exist')
            return HttpResponseRedirect('/')
        redirect_url = '/books'
        if book.assigned_to is request.user:
            message = messages.success(request, 'Book is Released from you')
        else:
            message = messages.error(request, 'Book is not assigned to you')
        return HttpResponseRedirect(redirect_url, {'message': message})