from __future__ import annotations

from django.contrib import admin
from django.core.exceptions import FieldDoesNotExist
from django.db import models
from django.utils import timezone
from django.utils.translation import get_language

from .jalali import (
    JalaliAdminDateWidget,
    JalaliAdminSplitDateTime,
    JalaliDateField,
    JalaliSplitDateTimeField,
    format_jalali,
)


def _is_persian() -> bool:
    return (get_language() or '').lower().split('-')[0] == 'fa'


class JalaliAdminMixin:
    """Add automatic Jalali dates to an admin while Persian is active.

    Keep this mixin before the concrete Django or third-party admin base class.
    """

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if _is_persian():
            if isinstance(db_field, models.DateTimeField):
                kwargs.update(form_class=JalaliSplitDateTimeField, widget=JalaliAdminSplitDateTime)
            elif isinstance(db_field, models.DateField):
                kwargs.update(form_class=JalaliDateField, widget=JalaliAdminDateWidget)
        return super().formfield_for_dbfield(db_field, request, **kwargs)

    def get_list_display(self, request):
        display = super().get_list_display(request)
        if not _is_persian():
            return display
        return tuple(self._jalali_column(item) for item in display)

    def _jalali_column(self, item):
        if not isinstance(item, str):
            return item
        try:
            field = self.model._meta.get_field(item)
        except FieldDoesNotExist:
            return item
        if not isinstance(field, models.DateField):
            return item

        include_time = isinstance(field, models.DateTimeField)

        @admin.display(description=field.verbose_name, ordering=item, empty_value='-')
        def jalali_value(obj):
            value = getattr(obj, item)
            if value is None:
                return None
            if include_time and timezone.is_aware(value):
                value = timezone.localtime(value)
            return format_jalali(value, include_time=include_time)

        # Keep the original name so explicit list_display_links continue to match.
        jalali_value.__name__ = item
        return jalali_value


class RichminAdmin(JalaliAdminMixin, admin.ModelAdmin):
    """Richmin's default ModelAdmin with Persian Jalali date support."""


class RichminStackedInline(JalaliAdminMixin, admin.StackedInline):
    """Stacked inline with Persian Jalali date widgets."""


class RichminTabularInline(JalaliAdminMixin, admin.TabularInline):
    """Tabular inline with Persian Jalali date widgets."""
