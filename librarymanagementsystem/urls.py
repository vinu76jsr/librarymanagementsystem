from django.conf.urls import patterns, include, url

from django.contrib import admin
from mainapp.views import BookListView, BookAssignView
from django.contrib.auth.decorators import login_required

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'librarymanagementsystem.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^accounts/profile/$', 'django.shortcuts.redirect', {'url': '/'}),
    url(r'^$', 'mainapp.views.index', name='index'),
    url(r'^logout/$', 'mainapp.views.logout_view', name='logout'),
    url(r'^login-error/$', 'mainapp.views.login_error', name='login_error'),
    url(r'^books/$', login_required(BookListView.as_view()), name='book-list'),
    # url(r'^books/(?P<book_id>\d+)/assign$', 'mainapp.views.book_assign', name='book-assign'),
    url(r'^books/(?P<book_id>\d+)/assign$', login_required(BookAssignView.as_view()), name='book-assign'),
    url(r'^books/(?P<book_id>\d+)/release', login_required(BookAssignView.as_view()), name='book-release'),


)
