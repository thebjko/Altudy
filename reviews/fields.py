from typing import Any, Optional, Sequence, Type, Union
from django import forms
from django.forms.widgets import Widget
from taggit.forms import TagWidget
from taggit.utils import parse_tags

class SpaceSeparatedTagsField(forms.CharField):
    widget = TagWidget()

    def clean(self, value):
        '''
        space separates tags
        '''
        tags = parse_tags(value)
        return super().clean(tags)
