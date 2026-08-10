from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.utils.timesince import timesince

from richmin.admin import RichminAdmin, RichminTabularInline
from richmin.admin_mixin import GlobalFilterMixin
from richmin.filters import DateInputFilter, InputFilter
from richmin.utils import attr
from .models import Author, Book, Genre
from ..loans.admin import BookLoanInline

admin.site.unregister(User)


class BooksInline(RichminTabularInline):
    model = Book


class PublishedOnFilter(DateInputFilter):
    title = 'Published on'
    parameter_name = 'published_on'


class ISBNFilter(InputFilter):
    title = 'ISBN'
    parameter_name = 'isbn'


@admin.register(Book)
class BookAdmin(GlobalFilterMixin, RichminAdmin):
    fieldsets = (
        (
            'general',
            {
                'fields': ('title', 'author', 'library'),
                'description': 'General book fields',
            },
        ),
        ('other', {'fields': ('genre', 'summary', 'isbn', 'published_on', 'published_at', 'pages')}),
    )
    raw_id_fields = ('author',)
    list_display = ('__str__', 'title', 'author', 'pages', 'published_on', 'published_at')
    readonly_fields = ('__str__',)
    list_per_page = 20
    list_max_show_all = 100
    list_editable = ('title',)
    list_filter = (ISBNFilter, PublishedOnFilter)
    search_fields = ('title', 'author__last_name')
    autocomplete_fields = ('genre',)
    date_hierarchy = 'published_on'
    save_as = True
    save_on_top = True
    inlines = (BookLoanInline,)

    actions_on_bottom = True

    # Order the sections within the change form
    richmin_section_order = ('book loans', 'general', 'other')

    global_filter = [
        ('library', 'library'),
    ]


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ('first_name', 'last_name', ('date_of_birth', 'date_of_death'))
    inlines = (BooksInline,)


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'object', 'action_flag', 'change_message', 'modified')
    readonly_fields = ['object', 'modified']
    search_fields = ('user__email',)
    date_hierarchy = 'action_time'
    list_filter = ('action_flag', 'content_type__model')
    list_per_page = 20

    def object(self, obj):
        url = obj.get_admin_url()
        return format_html(f'<a href="{url}">{obj.object_repr} [{obj.content_type.model}]</a>')

    @attr(admin_order_field='action_time')
    def modified(self, obj):
        if not obj.action_time:
            return 'Never'
        return f'{timesince(obj.action_time)} ago'


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    def get_queryset(self, request):
        """
        Remove our test user from the admin, so it cant be messed with
        """
        return super().get_queryset(request).exclude(username='test@test.com')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    search_fields = ('name',)
