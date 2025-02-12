class GlobalFilterMixin:
    """
    The GlobalFilterMixin should be the first class in the inheritance hierarchy.
    Example:
        class MyAdmin(GlobalFilterMixin, Foo, Bar)

    Each Item of the global filter must be a tuple. First item is the relation and the second item is model name.
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
        qs = self.apply_global_filter(request, qs)
        return qs

    def apply_global_filter(self, request, qs):
        if request.session.get('global_filters', {}):
            for relation, model_name in self.global_filter:
                relation: str

                if not relation.endswith('_id'):
                    relation = f'{relation}_id'

                value = request.session.get('global_filters').get(model_name, None)
                if not value:
                    continue
                qs = qs.filter(**{relation: value})
        return qs
