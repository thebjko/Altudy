from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings
from taggit.managers import TaggableManager
from multiselectfield import MultiSelectField
from django.core.exceptions import ValidationError

from django.utils import timezone
from datetime import timedelta

# Create your models here.
LANGUAGE_CHOICES = [
    ('py', 'Python'),
    ('java', 'Java'),
    ('js', 'JavaScript'),
    ('c', 'C'),
    ('c++', 'C++'),
    ('c#', 'C#'),
    ('ruby', 'Ruby'),
    ('dart', 'Dart'),
    ('scala', 'Scala'),
    ('go', 'Golang'),
    ('swift', 'Swift'),
    ('kotlin', 'Kotlin'),
    ('node_js', 'Node.js'),
]

STUDY_DAYS = [
    ('월', '월요일'),
    ('화', '화요일'),
    ('수', '수요일'),
    ('목', '목요일'),
    ('금', '금요일'),
    ('토', '토요일'),
    ('일', '일요일'),
]

class Study(models.Model):
    # 스터디장 유저
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='lead_studies')
    
    title = models.CharField(max_length=20)
    description = models.TextField(blank=True, null=True)
    # 스터디 주 언어
    language = MultiSelectField(choices=LANGUAGE_CHOICES, blank=True)
    category = TaggableManager(blank=True)
    # 스터디 최대 인원수
    capacity = models.PositiveSmallIntegerField(default=5, validators=[
        MaxValueValidator(10),
        MinValueValidator(2),
    ])
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    # 스터디 진행 요일
    days = MultiSelectField(choices=STUDY_DAYS, blank=True)
    # 스터디 진행 시작, 끝 시간
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    join_condition = models.PositiveSmallIntegerField(
        choices=[(1, '승인 필요'), (2, '바로 가입'), (3, '가입 불가'),],
        default=1
        )
    
    # 현재 모집 중인지 (정원 초과 or 가입 불가 선택)
    is_recruiting = models.PositiveSmallIntegerField(
        choices=[(1, '모집 중'), (2, '모집 마감'),],
        default=1
    )

    # 스터디 가입 요청
    join_request = models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='study_request', blank=True)
    
    # 스터디 참여중인 user, 중개테이블 - Studying
    studying_users = models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='user_studies', through='Studying', blank=True)

    post_index = models.IntegerField('게시글 번호', default=1)
    
    def __str__(self):
        return self.title
    
    @property
    def created_at_string(self):
        time = timezone.now() - self.created_at
        if time < timedelta(minutes=1):
            return '방금 전'
        elif time < timedelta(hours=1):
            return str(time.seconds // 60) + '분 전'
        elif time < timedelta(days=1):
            return str(time.seconds // 3600) + '시간 전'
        elif time < timedelta(days=30):
            return str(time.days) + '일 전'
        else:
            return self.created_at.strftime('%Y-%m-%d')
    

# study - user M:N 중개 테이블
class Studying(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    study = models.ForeignKey(to=Study, on_delete=models.CASCADE)
    
    permission = models.PositiveSmallIntegerField(default=1)
    joined_at = models.DateTimeField(auto_now_add=True)
    
    
class Announcement(models.Model):
    study = models.ForeignKey(to=Study, on_delete=models.CASCADE, related_name='announcements')
    
    title = models.CharField(max_length=20)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    announcement_reads = models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='user_reads', through='AnnouncementRead')
    
    @property
    def updated_at_string(self):
        time = timezone.now() - self.updated_at
        if time < timedelta(minutes=1):
            return '방금 전'
        elif time < timedelta(hours=1):
            return str(time.seconds // 60) + '분 전'
        elif time < timedelta(days=1):
            return str(time.seconds // 3600) + '시간 전'
        elif time < timedelta(days=30):
            return str(time.days) + '일 전'
        else:
            return self.updated_at.strftime('%Y-%m-%d')


class AnnouncementRead(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    announcement = models.ForeignKey(to=Announcement, on_delete=models.CASCADE)
    
    is_read = models.BooleanField(default=False)
    

# 라이브 스터디방(?) 테이블
# class Attendance(models.Model):
#     user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     class = models.ForeignKey(to=, on_delete=models.CASCADE)
    
#     start_time = models.TimeField(blank=True, null=True)
#     end_time = models.TimeField(blank=True, null=True)


class StudyComment(models.Model):
    study = models.ForeignKey(to=Study, on_delete=models.CASCADE)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    content = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    
    @property
    def created_at_string(self):
        time = timezone.now() - self.created_at
        if time < timedelta(minutes=1):
            return '방금 전'
        elif time < timedelta(hours=1):
            return str(time.seconds // 60) + '분 전'
        elif time < timedelta(days=1):
            return str(time.seconds // 3600) + '시간 전'
        elif time < timedelta(days=30):
            return str(time.days) + '일 전'
        else:
            return self.created_at.strftime('%Y-%m-%d')