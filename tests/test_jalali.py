from datetime import date, datetime

import pytest
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db import models
from django.test import RequestFactory
from django.utils import translation

from richmin.admin import RichminAdmin
from richmin.jalali import (
    JalaliAdminSplitDateTime,
    JalaliDateField,
    JalaliSplitDateTimeField,
    format_jalali,
    gregorian_to_jalali,
    jalali_to_gregorian,
)


@pytest.mark.parametrize(
    ('gregorian', 'jalali'),
    [
        (date(2024, 3, 20), (1403, 1, 1)),
        (date(2025, 3, 20), (1403, 12, 30)),
        (date(2025, 3, 21), (1404, 1, 1)),
        (date(1980, 1, 1), (1358, 10, 11)),
    ],
)
def test_jalali_conversion_round_trip(gregorian, jalali):
    assert gregorian_to_jalali(gregorian) == jalali
    assert jalali_to_gregorian(*jalali) == gregorian


def test_jalali_date_field_accepts_persian_digits():
    assert JalaliDateField().clean('۱۴۰۴/۰۱/۰۱') == date(2025, 3, 21)


def test_jalali_date_field_rejects_invalid_date():
    with pytest.raises(ValidationError):
        JalaliDateField().clean('1403/12/31')


def test_jalali_datetime_format():
    assert format_jalali(datetime(2025, 3, 21, 9, 7, 2), include_time=True) == '1404/01/01 09:07:02'


class DatedModel(models.Model):
    happened_on = models.DateField()
    happened_at = models.DateTimeField()

    class Meta:
        app_label = 'tests'

    def __str__(self):
        return str(self.happened_at)


class DatedAdmin(RichminAdmin):
    list_display = ('happened_on', 'happened_at')


def test_richmin_admin_uses_jalali_widgets_and_columns_in_persian():
    model_admin = DatedAdmin(DatedModel, admin.site)
    request = RequestFactory().get('/')
    with translation.override('fa'):
        date_formfield = model_admin.formfield_for_dbfield(DatedModel._meta.get_field('happened_on'), request)
        datetime_formfield = model_admin.formfield_for_dbfield(DatedModel._meta.get_field('happened_at'), request)
        columns = model_admin.get_list_display(request)

    assert isinstance(date_formfield, JalaliDateField)
    assert 'data-jdp' in date_formfield.widget.attrs
    assert date_formfield.widget.attrs['class'] == 'jalaliDateField'
    assert not date_formfield.widget.media._js
    assert isinstance(datetime_formfield, JalaliSplitDateTimeField)
    assert isinstance(datetime_formfield.widget, JalaliAdminSplitDateTime)
    assert datetime_formfield.widget.widgets[0].attrs['class'] == 'jalaliDateField'
    assert columns[0].admin_order_field == 'happened_on'
    assert columns[0].__name__ == 'happened_on'
    assert columns[1].admin_order_field == 'happened_at'
    assert columns[1].__name__ == 'happened_at'
    obj = DatedModel(happened_on=date(2025, 3, 21), happened_at=datetime(2025, 3, 21, 9, 7, 2))
    assert columns[0](obj) == '1404/01/01'


def test_richmin_admin_keeps_default_dates_outside_persian():
    model_admin = DatedAdmin(DatedModel, admin.site)
    request = RequestFactory().get('/')
    with translation.override('en'):
        formfield = model_admin.formfield_for_dbfield(DatedModel._meta.get_field('happened_on'), request)
        columns = model_admin.get_list_display(request)

    assert not isinstance(formfield, JalaliDateField)
    assert columns == ('happened_on', 'happened_at')
