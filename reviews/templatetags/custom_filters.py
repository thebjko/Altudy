import markdown as md
from django import template
from django.utils.safestring import mark_safe


register = template.Library()


@register.filter('dir')
def get_dir(obj):
    return dir(obj)

@register.filter
def markdown(value):
    extensions = ["nl2br", "fenced_code"]
    return mark_safe(md.markdown(value, extensions=extensions))


@register.filter('id')
def get_id(obj):
    return f'{obj.__class__.__name__}-{obj.pk}'


@register.filter('class')
def get_class_name(obj):
    return obj.__class__.__name__


@register.filter
def sort_by_likes(queryset):
    return sorted(queryset, key=lambda r: r.like_users.count(), reverse=True)