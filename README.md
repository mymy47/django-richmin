
# Django richmin (Rich Admin)

Drop-in theme for django admin, that utilises AdminLTE 3 & Bootstrap 4 to make yo' admin look richy

## Installation
```
pip install django-richmin
```

## Global Filter Usage
- First of all, add 'GlobalFilterMixin' to your admin model and put it in the first inheritance hierarchy e.g.
  ```
    from richmin.admin_mixin import GlobalFilterMixin
  
    class FooAdmin(GlobalFilterMixin, admin.ModelAdmin)
  ```
- Add 'global_filter' in your admin class. This field is a list of tuples.
  The first item of the tuple is the relation between model and field and the second item
  is the model name. Implement it like this:
  ```
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
- Using the latest [adminlte](https://adminlte.io/) + [bootstrap](https://getbootstrap.com/)

## Thanks
This was initially a Fork of https://github.com/farridav/django-jazzmin

- Based on AdminLTE 3: https://adminlte.io/
- Using Bootstrap 4: https://getbootstrap.com/
- Using Font Awesome 5: https://fontawesome.com/
