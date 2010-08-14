import json
from functools import wraps
from django.http import HttpResponse


def json_view(func):
    def wrap(request, *args, **kwargs):
        response = None
        response = func(request, *args, **kwargs)
        data = json.dumps(response)
        return HttpResponse(data, mimetype='application/json')
    return wrap
