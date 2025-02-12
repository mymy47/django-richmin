from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from richmin.settings import get_filter_models_keys


@login_required
def set_global_filter(request):
    keys = get_filter_models_keys()
    if request.method == "POST":
        if "global_filters" not in request.session:
            request.session["global_filters"] = {}

        for key in keys:
            if key in request.POST:
                request.session["global_filters"][key] = request.POST.get(key)

        # Mark the session as modified to ensure changes are saved
        request.session.modified = True

    return redirect(request.META.get("HTTP_REFERER", "admin:index"))
