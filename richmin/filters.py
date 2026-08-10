from django import forms
from django.contrib import admin, messages
from django.core.exceptions import ValidationError
from django.utils.translation import get_language

from .jalali import JalaliDateField


class InputFilter(admin.SimpleListFilter):
    template = 'admin/input_filter.html'
    title = ''
    parameter_name = ''
    has_validation_check = True

    def lookups(self, request, model_admin):
        return ((),)

    def queryset(self, request, queryset):
        value = self.value()
        if value:
            try:
                query = {self.parameter_name: self.clean_value(value)}
                if self.has_validation_check:
                    # Ensure query validity
                    queryset.filter(**query).only('id').first()
                return queryset.filter(**query)
            except (ValueError, ValidationError) as v:
                messages.error(request, str(v))
                return queryset.none()
        return queryset

    def clean_value(self, value):
        return value

    def choices(self, changelist):
        return []


class DateInputFilter(InputFilter):
    """A list filter with a Gregorian or Jalali date picker.

    Persian requests accept a Jalali date and convert it to the Gregorian
    ``date`` used by Django's ORM. Other languages use the browser's native
    date input and Django's normal date validation.
    """

    template = 'admin/date_input_filter.html'

    def __init__(self, request, params, model, model_admin):
        language_code = getattr(request, 'LANGUAGE_CODE', '') or get_language() or ''
        self.is_jalali = language_code.lower().split('-', 1)[0] == 'fa'
        super().__init__(request, params, model, model_admin)

    def clean_value(self, value):
        field = JalaliDateField() if self.is_jalali else forms.DateField()
        return field.clean(value)
