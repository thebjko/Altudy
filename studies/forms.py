from django import forms
from .models import Study, Announcement, Studying
from taggit.forms import TagWidget, TagField

from reviews.fields import SpaceSeparatedTagsField

class StudyForm(forms.ModelForm):    
    class Meta:
        model = Study
        fields = (
            'title', 
            'description',
            'language',
            'category',
            'capacity',
            'start_date',
            'end_date',
            'days',
            'start_time',
            'end_time',
            'join_condition',
            )
        labels = {
            # 'title': '', 
            # 'description': '',
            # 'language': '',
            # 'category': '',
            # 'capacity': '스터디 최대 인원수',
            # 'start_date': '스터디 시작일',
            # 'end_date': '스터디 종료일',
            # 'days': '스터디 진행 요일',
            # 'start_time': '스터디 시작시간',
            # 'end_time': '스터디 종료시간',
            # 'join_condition': '가입 요청 여부',
            }
        widgets = {
            'title': forms.TextInput(attrs={}),
            'description': forms.Textarea(attrs={}),
            'language': forms.SelectMultiple(attrs={}),
            'category': TagWidget(attrs={}),
            'capacity': forms.NumberInput(attrs={}),
            'start_date': forms.DateInput(attrs={'type':'date',}),
            'end_date': forms.DateInput(attrs={'type':'date',}),
            'days': forms.SelectMultiple(attrs={}),
            'start_time': forms.TimeInput(attrs={'type':'time',}),
            'end_time': forms.TimeInput(attrs={'type':'time',}),
            'join_condition': forms.Select(attrs={}),
        }
        help_texts = {
            'category': '태그를 입력하세요. 공백문자로 태그를 구분하며 대소문자를 구분하지 않습니다.',
            'capacity': '최대 인원 수는 10명입니다.',
        }


    # 정원을 현재 스터디 인원보다 낮게 수정하려 하는 경우 capacity 필드에 에러메시지 전송
    def clean(self):
        cleaned_data = super().clean()
        capacity = cleaned_data.get('capacity')
        studying_count = Studying.objects.filter(study=self.instance).count()

        if capacity and studying_count > capacity:
            self.add_error('capacity', f"현재 스터디 인원({studying_count}명)보다 정원을 줄일 수 없습니다.")
        
        
class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ('title', 'content',)
        labels = {
            # 'title': '',
            # 'content': '',
        }
        widgets = {
            'title': forms.TextInput(attrs={}),
            'content': forms.Textarea(attrs={}),
        }