from studies.models import Study, Studying, Announcement
from django.utils import timezone
from datetime import timedelta

def alarm(request):
    if request.user.is_authenticated:
        lead_studies = Study.objects.filter(user=request.user)
        all_requests = list()
        requests_exist = False
        for study in lead_studies:
            all_requests.append((study, study.join_request.all()))
            requests_exist = study.join_request.all().exists() or requests_exist
        
        all_announcements = list()
        announcements_exist = False
        studyings = Studying.objects.filter(user=request.user)
        for studying in studyings:
            announcements = Announcement.objects.filter(
                        study=studying.study, 
                        updated_at__gte=timezone.now() - timedelta(days=7),
                        announcementread__is_read=False,
                        announcementread__user=request.user,
                        )
            all_announcements.append((studying.study, announcements))
            announcements_exist = announcements.exists() or announcements_exist

        context = {
            'all_requests': all_requests,
            'all_announcements': all_announcements,
            'requests_exist': requests_exist,
            'announcements_exist': announcements_exist,
        }
    else:
        context = {

        }

    return context