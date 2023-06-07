from django import forms
from taggit.forms import TagWidget, TagField

from .models import Problem, Review, Comment
    

class ProblemForm(forms.ModelForm):
    '''
    태그 help_text 한 곳에서 관리하기
    '''
    tags = TagField(
        required=False,
        widget=TagWidget,
        help_text='태그를 입력하세요. 공백문자로 태그를 구분하며 대소문자를 구분하지 않습니다.',
    )
    class Meta:
        model = Problem
        fields = (
            'title',
            'url',
            'tags',
            'description',
        )


class ReviewForm(forms.ModelForm):
    tags = TagField(
        required=False,
        widget=TagWidget,
        help_text = '태그를 입력하세요. 공백문자로 태그를 구분하며 대소문자를 구분하지 않습니다.',
    )
    class Meta:
        model = Review
        fields = (
            'tags',
            'content',
        )


class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ('content', 'tags')
