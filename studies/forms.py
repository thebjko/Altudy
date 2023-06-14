from django import forms
from .models import Study, Announcement, Studying, StudyComment
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
            'title': '스터디 이름', 
            'description': '스터디 설명',
            'language': '언어',
            'category': '카테고리',
            'capacity': '모집 인원',
            'start_date': '스터디 시작일',
            'end_date': '스터디 종료일',
            'days': '진행 요일',
            'start_time': '시작 시간',
            'end_time': '종료 시간',
            'join_condition': '가입 요청',
            }
        widgets = {
            'title': forms.TextInput(attrs={
                'class':'title',
                'placeholder':'스터디 이름을 입력하세요',
            }),
            'description': forms.Textarea(attrs={
                'class':'description',
                'placeholder':'스터디 설명을 입력하세요\r\n \r\n- 스터디 목적/주제: [스터디 목적/주제]\r\n- 참여 조건 및 요구사항: [참여 조건/요구사항]\r\n- 스터디 활동 내용: [스터디 활동 내용]\r\n\r\n자세한 설명을 추가하시면, 더 멋진 스터디원을 구하는데 도움이 됩니다.',
            }),
            'language': forms.SelectMultiple(attrs={
                'class':'language',
            }),
            'category': TagWidget(attrs={
                'class':'category',
                'placeholder':'ex) 비대면, 소규모, 코테준비 등',
            }),
            'capacity': forms.NumberInput(attrs={
                'class':'capacity',
            }),
            'start_date': forms.DateInput(attrs={
                'class':'start_date',
                'type':'date',
            }),
            'end_date': forms.DateInput(attrs={
                'class':'end_date',
                'type':'date',
            }),
            'days': forms.SelectMultiple(attrs={
                'class':'days',
            }),
            'start_time': forms.TimeInput(attrs={
                'class':'start_time',
                'type':'time',
            }),
            'end_time': forms.TimeInput(attrs={
                'class':'end_time',
                'type':'time',
            }),
            'join_condition': forms.Select(attrs={
                'class':'join_condition',
            }),
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
            'title': '',
            'content': '',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class':'title',
                'placeholder': '공지 제목을 입력해주세요',
            }),
            'content': forms.Textarea(attrs={
                'class':'content',
                'placeholder': '공지 내용을 입력해주세요',
            }),
        }
        
        
class StudyCommentForm(forms.ModelForm):
    class Meta:
        model = StudyComment
        fields = ('content',)
        labels = {
            # 'content': '',
        }
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': '1',
                'placeholder': '댓글을 입력하세요',
                'class': 'comment-form',
                }),
        }