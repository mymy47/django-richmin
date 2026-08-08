from __future__ import annotations

from datetime import date, datetime

from django import forms
from django.contrib.admin.widgets import AdminDateWidget, AdminSplitDateTime
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def gregorian_to_jalali(value: date) -> tuple[int, int, int]:
    """Convert a Gregorian date to a Solar Hijri (Jalali) date."""
    gy, gm, gd = value.year, value.month, value.day
    g_days = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
    gy2 = gy + 1 if gm > 2 else gy
    days = 355666 + (365 * gy) + ((gy2 + 3) // 4) - ((gy2 + 99) // 100) + ((gy2 + 399) // 400) + gd
    days += g_days[gm - 1]
    jy = -1595 + (33 * (days // 12053))
    days %= 12053
    jy += 4 * (days // 1461)
    days %= 1461
    if days > 365:
        jy += (days - 1) // 365
        days = (days - 1) % 365
    if days < 186:
        jm, jd = 1 + (days // 31), 1 + (days % 31)
    else:
        jm, jd = 7 + ((days - 186) // 30), 1 + ((days - 186) % 30)
    return jy, jm, jd


def jalali_to_gregorian(year: int, month: int, day: int) -> date:
    """Convert a Solar Hijri (Jalali) date to a Gregorian date."""
    jy = year + 1595
    days = -355668 + (365 * jy) + ((jy // 33) * 8) + (((jy % 33) + 3) // 4) + day
    days += (month - 1) * 31 if month < 7 else ((month - 7) * 30) + 186
    gy = 400 * (days // 146097)
    days %= 146097
    if days > 36524:
        days -= 1
        gy += 100 * (days // 36524)
        days %= 36524
        if days >= 365:
            days += 1
    gy += 4 * (days // 1461)
    days %= 1461
    if days > 365:
        gy += (days - 1) // 365
        days = (days - 1) % 365
    gd = days + 1
    leap = gy % 4 == 0 and (gy % 100 != 0 or gy % 400 == 0)
    month_days = [31, 29 if leap else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    gm = 1
    for length in month_days:
        if gd <= length:
            break
        gd -= length
        gm += 1
    return date(gy, gm, gd)


def format_jalali(value: date | datetime, include_time: bool = False) -> str:
    jy, jm, jd = gregorian_to_jalali(value)
    result = f'{jy:04d}/{jm:02d}/{jd:02d}'
    if include_time and isinstance(value, datetime):
        result += value.strftime(' %H:%M:%S')
    return result


def _ascii_digits(value: str) -> str:
    return value.translate(str.maketrans('۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩', '01234567890123456789'))


class JalaliDateField(forms.DateField):
    default_error_messages = {'invalid': _('Enter a valid Jalali date in YYYY/MM/DD format.')}

    def to_python(self, value):
        if value in self.empty_values or isinstance(value, datetime):
            return value.date() if isinstance(value, datetime) else None
        if isinstance(value, date):
            return value
        try:
            parts = _ascii_digits(str(value).strip()).replace('-', '/').split('/')
            if len(parts) != 3:
                raise ValueError
            year, month, day = (int(part) for part in parts)
            converted = jalali_to_gregorian(year, month, day)
            if gregorian_to_jalali(converted) != (year, month, day):
                raise ValueError
            return converted
        except (TypeError, ValueError, OverflowError):
            raise ValidationError(self.error_messages['invalid'], code='invalid')


class JalaliAdminDateWidget(AdminDateWidget):
    class Media:
        # Richmin loads the Jalali picker globally for Persian pages. In particular,
        # don't load Django's Gregorian DateTimeShortcuts for this widget.
        extend = False
        css = {}
        js = []

    def __init__(self, attrs=None, format=None):
        attrs = {
            'class': 'jalaliDateField',
            **(attrs or {}),
            'data-jdp': '',
            'autocomplete': 'off',
            'placeholder': 'YYYY/MM/DD',
        }
        super().__init__(attrs=attrs, format=format)

    def format_value(self, value):
        if isinstance(value, datetime):
            value = value.date()
        return format_jalali(value) if isinstance(value, date) else value


class JalaliSplitDateTimeField(forms.SplitDateTimeField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        original = self.fields[0]
        self.fields = (
            JalaliDateField(required=original.required, disabled=original.disabled, localize=original.localize),
            self.fields[1],
        )


class JalaliAdminSplitDateTime(AdminSplitDateTime):
    def __init__(self, attrs=None):
        super().__init__(attrs)
        self.widgets[0] = JalaliAdminDateWidget(attrs=attrs)
