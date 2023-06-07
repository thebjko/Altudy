from django import template
from django.utils import timezone
from datetime import timedelta

from studies.models import Study, Studying, Announcement

register = template.Library()

@register.filter(name="test")
def test(value, arg):
    return value + '"te+st"' + arg


@register.filter(name="alarm_exists")
def alarm_exists(me):
    # 스터디 가입 요청
    studies = Study.objects.filter(user=me)
    for study in studies:
        if study.join_request.exists():
            return True
        
    # 기타 알람이 갈 수 있는 사항들(스터디 공지사항 등)
    studyings = Studying.objects.filter(user=me)
    for studying in studyings:
        announcements = Announcement.objects.filter(
            study=studying.study, 
            updated_at__gte=timezone.now() - timedelta(days=7),
            announcementread__is_read=False,
            announcementread__user=me,
            )
        if announcements.exists():
            return True

    return False