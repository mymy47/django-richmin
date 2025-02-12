from richmin.views import set_global_filter
from django.urls import path

set_filter_path = [
    path('set-global-filter', set_global_filter, name='set_global_filter')
]
