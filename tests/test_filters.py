from datetime import date

import pytest
from django.urls import reverse

from .test_app.library.factories import BookFactory


@pytest.mark.django_db
def test_input_filter_filters_an_exact_value(admin_client):
    matching = BookFactory(isbn='9780123456786')
    other = BookFactory(isbn='9780987654321')

    response = admin_client.get(reverse('admin:books_book_changelist'), {'isbn': '9780123456786'})
    content = response.content.decode()

    assert response.status_code == 200
    assert 'name="isbn"' in content
    assert 'placeholder="ISBN"' in content
    assert matching in response.context['cl'].result_list
    assert other not in response.context['cl'].result_list


@pytest.mark.django_db
def test_date_input_filter_uses_admin_picker_and_filters_gregorian_dates(admin_client):
    matching = BookFactory(published_on=date(2025, 3, 21))
    other = BookFactory(published_on=date(2025, 3, 22))

    response = admin_client.get(reverse('admin:books_book_changelist'), {'published_on': '2025-03-21'})
    content = response.content.decode()

    assert response.status_code == 200
    assert 'name="published_on"' in content
    assert 'class="form-control vDateField"' in content
    assert 'placeholder="Published on"' in content
    assert matching in response.context['cl'].result_list
    assert other not in response.context['cl'].result_list


@pytest.mark.django_db
def test_date_input_filter_uses_jalali_picker_and_converts_value(admin_client):
    matching = BookFactory(published_on=date(2025, 3, 21))
    other = BookFactory(published_on=date(2025, 3, 22))

    response = admin_client.get(
        reverse('admin:books_book_changelist'),
        {'published_on': '1404/01/01'},
        HTTP_ACCEPT_LANGUAGE='fa',
    )
    content = response.content.decode()

    assert response.status_code == 200
    assert 'name="published_on"' in content
    assert 'jalaliDateField' in content
    assert 'data-jdp' in content
    assert 'placeholder="Published on"' in content
    assert 'YYYY/MM/DD' not in content
    assert matching in response.context['cl'].result_list
    assert other not in response.context['cl'].result_list


@pytest.mark.django_db
def test_date_input_filter_rejects_an_invalid_date(admin_client):
    BookFactory(published_on=date(2025, 3, 21))

    response = admin_client.get(reverse('admin:books_book_changelist'), {'published_on': 'not-a-date'})

    assert response.status_code == 200
    assert list(response.context['cl'].result_list) == []
