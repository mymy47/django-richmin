
# Django richmin (Rich Admin)

Drop-in theme for django admin, that utilises AdminLTE 3 & Bootstrap 4 to make yo' admin look richy

## Installation
```shell
pip install django-richmin
```

## Releasing

Install the release tools once:

```shell
python -m pip install -r requirements.release.txt
```

After updating the package version, build, validate, and upload the release to
PyPI with one command on Windows, Linux, or macOS:

```shell
python release.py
```

Twine will use your configured PyPI credentials or prompt for them. The script
removes old generated files from `build/` and `dist/` before building, so only
the current release is uploaded. Uploads are verbose and safe to retry: files
that PyPI already accepted are skipped while any remaining files are uploaded.

#### Support Iframe in admin popups

Add this config to django settings.py:
```python
X_FRAME_OPTIONS = 'SAMEORIGIN'
```

## Global Filter Usage
- First of all, add 'GlobalFilterMixin' to your admin model and put it in the first inheritance hierarchy e.g.
  ```python
    from richmin.admin_mixin import GlobalFilterMixin
  
    class FooAdmin(GlobalFilterMixin, admin.ModelAdmin)
  ```
- Add 'global_filter' in your admin class. This field is a list of tuples.
  The first item of the tuple is the relation between model and field and the second item
  is the model name. Implement it like this:
  ```python
    global_filters = [
      ('bar', 'bar'),
      ('bar__baz', 'baz'),
    ]
  ```

## Features
- Drop-in admin skin, all configuration optional
- Customisable side menu
- Customisable top menu
- Customisable user menu
- 4 different Change form templates (horizontal tabs, vertical tabs, carousel, collapsible)
- Bootstrap 4 modal (instead of the old popup window, optional)
- Search bar for any given model admin
- Customisable UI (via Live UI changes, or custom CSS/JS)
- Responsive
- Select2 drop-downs
- Bootstrap 4 & AdminLTE UI components
- Support dark theme
- Navbar filter

## Theme configuration

Richmin uses the modern theme by default. To restore the original Richmin
appearance, select the legacy theme in Django settings:

```python
RICHMIN_SETTINGS = {
    'theme': 'legacy',
}
```

Available themes are `default` and `legacy`. Each theme provides an independent
light and dark stylesheet, while the Auto/Light/Dark toggle controls which mode
is active.

## Thanks
This was initially a Fork of https://github.com/farridav/django-jazzmin

- Based on AdminLTE 3: https://adminlte.io/
- Using Bootstrap 4: https://getbootstrap.com/
- Using Font Awesome 5: https://fontawesome.com/

# Jalali dates in the Persian admin

When Persian (`fa`) is the active language, inherit model admins from `RichminAdmin` to use a Jalali date picker for
`DateField` and `DateTimeField` form inputs and Jalali formatting for those fields in change-list tables. Database values
remain ordinary Gregorian Django dates.

```python
from richmin.admin import RichminAdmin

@admin.register(Event)
class EventAdmin(RichminAdmin):
    list_display = ('name', 'starts_at')
```

`RichminAdmin` is the recommended base for regular model admins. For an admin that must already inherit from another
base, put `JalaliAdminMixin` first. Jalali-ready stacked and tabular inline bases are also available:

```python
from django.contrib.auth.admin import UserAdmin
from richmin.admin import JalaliAdminMixin, RichminTabularInline

class CustomUserAdmin(JalaliAdminMixin, UserAdmin):
    pass

class EventInline(RichminTabularInline):
    model = Event
```
