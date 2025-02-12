from richmin.settings import get_filter_models


def global_filter_context(request):
    filter_model_dict = get_filter_models()
    if not filter_model_dict:
        return {}

    selected_filters = {}
    for key in filter_model_dict.keys():
        selected_filters[key.lower()] = request.session.get('global_filters', {}).get(f"{key.lower()}")
    return {"filter_queryset": filter_model_dict, "selected_keys": selected_filters}
