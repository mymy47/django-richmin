from django.conf import settings
from django.test import override_settings

from richmin.settings import get_search_model_string, get_settings


def test_get_search_model_string():
    # model name is always lower case
    assert get_search_model_string('books.Book') == 'books.book'
    assert get_search_model_string('books.book') == 'books.book'
    # the app name gets never touched
    assert get_search_model_string('Books.Book') == 'Books.book'
    assert get_search_model_string('BookShelf.book') == 'BookShelf.book'


def test_default_theme_has_light_and_dark_stylesheets():
    richmin_settings = get_settings()

    assert richmin_settings['theme'] == 'default'
    assert richmin_settings['theme_css'] == {
        'light': 'richmin/css/themes/default/light.css',
        'dark': 'richmin/css/themes/default/dark.css',
    }


def test_legacy_theme_has_light_and_dark_stylesheets():
    configured = {**settings.RICHMIN_SETTINGS, 'theme': 'legacy'}

    with override_settings(RICHMIN_SETTINGS=configured):
        richmin_settings = get_settings()

    assert richmin_settings['theme'] == 'legacy'
    assert richmin_settings['theme_css'] == {
        'light': 'richmin/css/themes/legacy/light.css',
        'dark': 'richmin/css/themes/legacy/dark.css',
    }


def test_unknown_theme_falls_back_to_default():
    configured = {**settings.RICHMIN_SETTINGS, 'theme': 'unknown'}

    with override_settings(RICHMIN_SETTINGS=configured):
        richmin_settings = get_settings()

    assert richmin_settings['theme'] == 'default'
