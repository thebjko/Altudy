from django.http import HttpResponse
from django.template import loader
from typing import Any


class HXResponse(HttpResponse):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        trigger = kwargs.pop('trigger')
        super().__init__(*args, **kwargs)
        self.headers["HX-Trigger"] = trigger


def render_HXResponse(request, template_name, context=None, content_type=None, status=None, using=None, trigger=None):
    content = loader.render_to_string(template_name, context, request, using=using)
    response = HXResponse(content, content_type, status, trigger=trigger)
    return response
