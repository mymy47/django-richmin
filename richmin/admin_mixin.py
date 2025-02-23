class GlobalFilterMixin:
    """
    The GlobalFilterMixin should be the first class in the inheritance hierarchy.
    Example:
        class MyAdmin(GlobalFilterMixin, Foo, Bar)

    Each Item of the global filter must be a tuple.
    The First item is the relation and the second item is model name.
    Example:
        class FooAdmin(GlobalFilterMixin, admin.ModelAdmin):
            global_filter = [
                ('project__organization', 'organization'),
                ('project', 'project'),
            ]
    """
    global_filter = []

    def get_queryset(self, request):
        qs = super().get_queryset(request)  # noqa
        if not request.path.endswith('/change/'):  # Ignore global filter in change form page
            qs = self.apply_global_filter(request, qs)
        return qs

    def apply_global_filter(self, request, qs):
        for relation, model_name in self.global_filter:
            value = request.COOKIES.get(f'richy_global_filter_{model_name.lower()}')
            if not value:
                continue
            if not relation.endswith('_id'):
                relation = f'{relation}_id'
            qs = qs.filter(**{relation: value})
        return qs
