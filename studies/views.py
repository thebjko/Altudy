from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from taggit.models import Tag
from django.db.models import Count
from django.contrib import messages
from django.db.models import Q
from datetime import datetime, timedelta
from django.utils import timezone
from django.http import JsonResponse

from reviews.models import Problem, Review
from .models import Study, Studying, Announcement, AnnouncementRead
from .forms import StudyForm, AnnouncementForm
from .models import LANGUAGE_CHOICES
from django.db.models import Q
import re


# Create your views here.
def index(request):
    studies = Study.objects.annotate(
        member_num=Count('studying_users')
        ).order_by('-created_at')
    
    selected_langs = request.GET.get('lang')
    is_recruit = request.GET.get('recruits')
    if is_recruit == 'true':
        studies = studies.filter(is_recruiting=1)

    if selected_langs:
        selected_langs_list = selected_langs.split(',') 
        filter_query = Q()
        for lang in selected_langs_list:
            filter_query |= Q(language__regex=r'\b{}\b'.format(re.escape(lang.strip())))
        studies = studies.filter(filter_query).distinct()
        print(studies)

    context = {
        'studies': studies,
        'LANGUAGE_CHOICES' : LANGUAGE_CHOICES,
    }
    return render(request, 'studies/index.html', context)


def detail(request, study_pk: int):
    study = get_object_or_404(Study, pk=study_pk)
    
    # 현재 스터디 가입 여부 is_studying
    if study.studying_users.filter(pk=request.user.pk).exists():
        # 스터디 가입
        is_studying = 'joined'
    elif study.join_request.filter(pk=request.user.pk).exists():
        is_studying = 'join_request'
    else:
        # 스터디 미가입
        is_studying = 'not_joined'
    
    context = {
        'study': study,
        'is_studying': is_studying,
        'LANGUAGE_CHOICES': LANGUAGE_CHOICES,
    }
    return render(request, 'studies/detail.html', context)


@login_required
def create(request):
    if request.method == 'POST':
        form = StudyForm(data=request.POST)
        if form.is_valid():
            study = form.save(commit=False)
            study.user = request.user
            study.save()
            
            # Tag 저장
            form.save_m2m()
            
            # 스터디장 권한(permission) 3으로 Studying 테이블에 추가
            # 임시 스터디장 혹은 부스터디장 권한(permission) 2 예정
            Studying.objects.create(study=study, user=request.user, permission=3)
            
            return redirect('studies:detail', study.pk)
    else:
        form = StudyForm()
        
    context = {
        'form': form,
    }
    return render(request, 'studies/create.html', context)


def update(request, study_pk: int):
    study = get_object_or_404(Study, pk=study_pk)
    
    # 스터디장만 수정 가능
    if request.user != study.user:
        return redirect('studies:detail', study_pk)
    
    if request.method == 'POST':
        form = StudyForm(data=request.POST, instance=study)
        if form.is_valid():
            # taggit을 위해 commit=False 후 save_m2m()
            study = form.save(commit=False)
            # 스터디 가입 조건-가입 불가로 변경시 모든 가입 요청 삭제, 모집 마감
            if study.join_condition == 3:
                study.join_request.clear()
                study.is_recruiting = 2

            # 스터디 정원 늘어난 경우 - 가입 불가 상태가 아니고, 기존에 모집 마감상태였다면 모집 중으로 다시 변경
            if Studying.objects.filter(study=study).aggregate(cnt=Count('*'))['cnt'] < study.capacity and study.join_condition != 3 and study.is_recruiting == 2:
                study.is_recruiting = 1
            # 스터디 정원을 현재 인원만큼 줄인 경우 - 가입 불가 상태가 아니고, 기존에 모집 중 상태였다면 모집 마감으로 다시 변경
            elif Studying.objects.filter(study=study).aggregate(cnt=Count('*'))['cnt'] == study.capacity and study.join_condition != 3 and study.is_recruiting == 1:
                study.is_recruiting = 2
            
            study.save()
            form.save_m2m()
            
            return redirect('studies:detail', study_pk)
    else:
        form = StudyForm(instance=study)
        
    context = {
        'study_pk': study_pk,
        'form': form,
    }
    return render(request, 'studies/update.html', context)


def delete(request, study_pk: int):
    study = get_object_or_404(Study, pk=study_pk)
    
    # 스터디장만 삭제 가능
    if request.user == study.user:
        try:
            study.delete()
            return redirect('/')
        finally:
            Tag.objects.annotate(ntag=Count('taggit_taggeditem_items')).filter(ntag=0).delete()
        
    
    return redirect('studies:index')


# 스터디 가입 및 가입 요청
@login_required
def join(request, study_pk: int):
    study = get_object_or_404(Study, pk=study_pk)
    me = request.user
    
    # 스터디 인원 만원 시 승낙 불가
    if Studying.objects.filter(study=study).aggregate(cnt=Count('*'))['cnt'] >= study.capacity:
        print('Error: 스터디 만원')
        return redirect('studies:detail', study_pk)
    
    # User가 스터디에 가입되어 있지 않은 경우
    if not Studying.objects.filter(study=study, user=me).exists():
        # 1 : 승인 필요, 2: 즉시 가입, 3: 가입 불가
        if study.join_condition == 2:
            # Studying.objects.create(study=study, user=me)
            study.studying_users.add(me)
            # AnnouncementRead 공지 읽음 여부 테이블에 추가
            for announcement in study.announcements.all():
                announcement.announcement_reads.add(me)
        elif study.join_condition == 1:
            study.join_request.add(me)
        # join_condition == 3 - 가입불가
    
    # 가입 후 스터디 인원 만원 시 모집 마감
    if Studying.objects.filter(study=study).aggregate(cnt=Count('*'))['cnt'] >= study.capacity:
        study.is_recruiting = 2
        study.save()

    return redirect('studies:detail', study_pk)
    

# 스터디 탈퇴
@login_required
def withdraw(request, study_pk: int):
    study = get_object_or_404(Study, pk=study_pk)
    me = request.user
    
    if study.studying_users.filter(pk=me.pk).exists():
        # 스터디장 탈퇴 불가
        if me != study.user:
            study.studying_users.remove(me)
    
    # 탈퇴 후에 정원이 남아있고, 가입 불가 상태가 아니고, 모집 마감상태라면 모집 중으로 다시 변경
    if Studying.objects.filter(study=study).aggregate(cnt=Count('*'))['cnt'] < study.capacity and study.join_condition != 3 and study.is_recruiting == 2:
        study.is_recruiting = 1
        study.save()
        
    return redirect('studies:detail', study_pk)


# 스터디 가입 요청 시 수락
@login_required
def accept(request, study_pk: int, username: int):
    study = get_object_or_404(Study, pk=study_pk)
    person = get_user_model().objects.get(username=username)
    me = request.user
    
    # Study 가입 조건-가입 불가 시 가입 요청 승인 불가
    if study.join_condition == 3:
        return redirect('studies:detail', study_pk)
        
    # 스터디 인원 만원 시 승낙 불가
    if Studying.objects.filter(study=study).aggregate(cnt=Count('*'))['cnt'] >= study.capacity:
        print('Error: 스터디 만원')
        return redirect('studies:detail', study_pk)
    
    # 스터디장 혹은 부스터디장(permission > 1)인 유저만 요청 허가 가능
    if Studying.objects.filter(study=study, user=me, permission__gte=2).exists():
        Studying.objects.get_or_create(study=study, user=person)
        for announcement in study.announcements.all():
            announcement.announcement_reads.add(person)
        study.join_request.remove(person)
    
    # 가입 후 스터디 인원 만원 시 모집 마감
    if Studying.objects.filter(study=study).aggregate(cnt=Count('*'))['cnt'] >= study.capacity:
        study.is_recruiting = 2
        study.save()

    return redirect('studies:detail', study_pk)

# 스터디 가입 요청 시 거절
@login_required
def reject(request, study_pk: int, username: int):
    study = get_object_or_404(Study, pk=study_pk)
    person = get_user_model().objects.get(username=username)
    me = request.user
    
    # 스터디장 혹은 부스터디장(permission > 1)인 유저만 스터디 가입 요청 거절
    if Studying.objects.filter(study=study, user=me, permission__gte=2).exists():
        study.join_request.remove(person)
    
    return redirect('studies:detail', study_pk)


# 스터디에서 해당 유저 방출
@login_required
def expel(request, study_pk: int, username: int):
    study = get_object_or_404(Study, pk=study_pk)
    person = get_user_model().objects.get(username=username)
    me = request.user
    
    # 스터디장인 유저만 스터디원 방출 가능
    if Studying.objects.filter(study=study, user=me, permission__gte=2).exists():
        studying = Studying.objects.filter(study=study, user=person)
        if studying.first().permission <= 2:
            studying.first().delete()
    

    # 방출 후에 정원이 남아있고, 가입 불가 상태가 아니고, 모집 마감상태라면 모집 중으로 다시 변경
        if Studying.objects.filter(study=study).aggregate(cnt=Count('*'))['cnt'] < study.capacity and study.join_condition != 3 and study.is_recruiting == 2:
            study.is_recruiting = 1
            study.save()

    return redirect('studies:detail', study_pk)


# 스터디 가입 요청 취소
@login_required
def cancel(request, study_pk: int):
    study = get_object_or_404(Study, pk=study_pk)
    me = request.user
    
    if study.join_request.filter(pk=me.pk).exists():
        study.join_request.remove(me)
    
    return redirect('studies:detail', study_pk)


@login_required
def mainboard(request, study_pk: int):
    request.session['study_id'] = study_pk
    study = get_object_or_404(Study, pk=study_pk)
    users = study.studying_users.all()

    # 스터디에 가입되어있지 않으면 접근 불가
    if not Studying.objects.filter(study=study, user=request.user).exists():
        return redirect('studies:detail', study_pk)

    # 메인보드에서는 이번주에 추가된 문제만 보여주도록? 일단 임의로 추가
    # start_of_week = datetime.now().date() - timedelta(days=datetime.now().weekday())
    ## Warning : warnings.warn("DateTimeField %s received a naive datetime (%s)"
    ## 계산될 시간에 datetime.now() 대신 timezone.now() 사용해봤음
    start_of_week = timezone.now() - timedelta(days=datetime.now().weekday())
    end_of_week = start_of_week + timedelta(days=6)
    problems = Problem.objects.filter(study=study, created_at__range=(start_of_week, end_of_week))

    # 유저별 리뷰 수, 백분율 (그래프에 사용)
    user_reviews = {}
    user_percentages = {}
    total_reviews = 0

    for user in users:
            reviews_count = Review.objects.filter(problem__study=study, user=user).count()
            user_reviews[user.username] = reviews_count
            total_reviews += reviews_count

    for user, reviews_count in user_reviews.items():
            if total_reviews:
                # Division 0 Error 발생 가능
                percentage = (reviews_count / total_reviews) * 100
            else:
                percentage = 0
            user_percentages[user] = int(percentage)

    user_reviews = sorted(user_reviews.items(), key=lambda x: x[1], reverse=True)
    user_percentages = sorted(user_percentages.items(), key=lambda x: x[1], reverse=True)

    # 메인보드에서 보여줄 공지
    announcements = Announcement.objects.filter(study=study)
    
    context = {
        'problems': problems,
        'study': study,
        'announcements': announcements,
        'users': users,
        'user_reviews': user_reviews,
        'user_percentages': user_percentages,
    }
    return render(request, 'studies/mainboard.html', context)


@login_required
def member(request, study_pk: int):
    study = get_object_or_404(Study, pk=study_pk)

    # 스터디장만 접근 가능
    if not Studying.objects.filter(study=study, user=request.user, permission__gte=2).exists():
        return redirect('studies:mainboard', study_pk)
    
    users = study.studying_users.all().order_by('-studying__permission')
    join_requests = study.join_request.all()
    study_members = Studying.objects.filter(study=study)
    print(study_members)

    context = {
        'study': study,
        'study_members': study_members,
        'join_requests': join_requests,
    }
    return render(request, 'studies/member.html', context)


@login_required
def problem(request, study_pk: int):
    study = get_object_or_404(Study, pk=study_pk)
    query = request.GET.get('query')
    problems = Problem.objects.filter(study=study)

    # 스터디에 가입되어있지 않으면 접근 불가
    if not Studying.objects.filter(study=study, user=request.user).exists():
        return redirect('studies:detail', study_pk)
    
    if query:
        problems = problems.filter(title__icontains=query)

    context = {
        'study': study,
        'problems': problems,
    }
    return render(request, 'studies/problem.html', context)


@login_required
def problem_search(request, study_pk: int):
    study = get_object_or_404(Study, pk=study_pk)
    query = request.GET.get('query')
    isSolved = request.GET.get('isSolved')
    problems = Problem.objects.filter(study=study)

    # 제출하지 않은 과제 버튼 on일때 문제 필터링
    if isSolved == 'true':
        # 현재 로그인한 유저가 작성한 리뷰의 문제 id 목록
        user_reviewed_problems = Review.objects.filter(user=request.user, problem__study=study).values('problem_id')

        if user_reviewed_problems:
            # 로그인한 유저가 리뷰를 남기지 않은 문제 목록
            problems = problems.exclude(id__in=user_reviewed_problems)

    if query:
        problems = problems.filter(
            Q(title__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()

    problems_list = []
    for problem in problems:
        problem_dict = {
            'title': problem.title,
            'id': problem.pk,
            # 원하는 정보 추가
        }
        problems_list.append(problem_dict)

    return JsonResponse({'problems': problems_list})


@login_required
def announcement(request, study_pk: int):
    study = get_object_or_404(Study, pk=study_pk)
    announcements = Announcement.objects.filter(study=study)
    
    # 스터디에 가입되어있지 않으면 접근 불가
    if not Studying.objects.filter(study=study, user=request.user).exists():
        return redirect('studies:detail', study_pk)
    
    context = {
        'announcements': announcements,    
        'study': study,
    }
    return render(request, 'studies/announcement.html', context)


def check_study_leader(request, leader: str, target_url: str, *url_args):
    # 스터디장만 announcement 생성, 수정, 삭제 가능
    if leader != request.user:
        print('Error : 스터디장 아님!')
        if url_args:
            return redirect(target_url, url_args)
        return redirect(target_url)
    

@login_required
def announcement_create(request, study_pk: int):
    study = get_object_or_404(Study, pk=study_pk)
    # check_study_leader(request, study.user, 'studies:announcement', study_pk)
    # 스터디장만 announcement 생성 가능
    if study.user != request.user:
        print('Error : 스터디장 아님!')
        return redirect('studies:announcement', study_pk)
    
    if request.method == 'POST':
        form = AnnouncementForm(data=request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.study = study
            announcement.save()
            
            # AnnouncementRead 공지 읽음 여부 테이블에 추가
            for person in study.studying_users.all():
                announcement.announcement_reads.add(person)
            
            return redirect('studies:announcement_detail', study_pk, announcement.pk)
    else:
        form = AnnouncementForm()
    
    context = {
        'form': form,
        'study_pk': study_pk,
    }
    return render(request, 'studies/announcement_create.html', context)


@login_required
def announcement_detail(request, study_pk: int, announcement_pk: int):
    announcement = get_object_or_404(Announcement, pk=announcement_pk)
    leader = get_object_or_404(Study, pk=study_pk).user
    
    # 읽음 상태로 전환
    announcement_read = AnnouncementRead.objects.get(announcement=announcement, user=request.user)
    announcement_read.is_read = True
    announcement_read.save()
    
    context = {
        'announcement': announcement,
        'study_pk': study_pk,
        'leader': leader,
    }
    return render(request, 'studies/announcement_detail.html', context)
    
    
@login_required
def announcement_update(request, study_pk: int, announcement_pk: int):
    study = get_object_or_404(Study, pk=study_pk)
    # check_study_leader(request, study.user, 'studies:announcement_detail', study_pk, announcement_pk)
    # 스터디장만 announcement 수정, 삭제 가능
    if study.user != request.user:
        return redirect('studies:announcement_detail', study_pk, announcement_pk)
    
    announcement = get_object_or_404(Announcement, pk=announcement_pk)
    
    if request.method == 'POST':
        form = AnnouncementForm(data=request.POST, instance=announcement)
        if form.is_valid():
            announcement = form.save()
            # 공지 업데이트 시 읽음 상태 초기화
            announcement_reads = AnnouncementRead.objects.filter(announcement=announcement)
            for announcement_read in announcement_reads:
                announcement_read.is_read = False
                announcement_read.save()
            
            return redirect('studies:announcement_detail', study_pk, announcement_pk)
    else:
        form = AnnouncementForm(instance = announcement)
    
    context = {
        'form': form,
        'study_pk': study_pk,
        'announcement_pk': announcement_pk,
    }
    return render(request, 'studies/announcement_update.html', context)
    

@login_required
def announcement_delete(request, study_pk: int, announcement_pk: int):
    study = get_object_or_404(Study, pk=study_pk)
    # check_study_leader(request, study.user, 'studies:announcement_detail', study_pk, announcement_pk)
    # 스터디장만 announcement 삭제 가능
    if study.user != request.user:
        return redirect('studies:announcement_detail', study_pk, announcement_pk)
    
    announcement = get_object_or_404(Announcement, pk=announcement_pk)
    announcement.delete()
    
    return redirect('studies:announcement', study_pk)


@login_required
def appoint(request, study_pk: int, username: str, permission: int):
    study = get_object_or_404(Study, pk=study_pk)
    person = get_user_model().objects.get(username=username)
    me = request.user 
    
    # 스터디장만 권한 부여 가능 + 자기 자신일때 취소
    if me != study.user or me == person:
        print('Error: 잘못된 접근!')
        return redirect('studies:mainboard', study_pk)
    
    # 스터디장 권한 양도
    if permission == 3:
        study.user = person
        study.save()
        new_leader = Studying.objects.get(study=study, user=person)
        new_leader.permission = 3
        old_leader = Studying.objects.get(study=study, user=me)
        old_leader.permission = 1
        new_leader.save()
        old_leader.save()
    # 부스터디장 임명
    elif permission == 2:
        study.studying_users.get(user=person).permission = 2

    return redirect('studies:mainboard', study_pk)


# 부스터디장 해임
@login_required
def dismiss(request, study_pk: int, username: str):
    study = get_object_or_404(Study, pk=study_pk)
    person = get_user_model().objects.get(username=username)
    me = request.user 
    
    # 스터디장만 타 유저 해임 가능 + 자기 자신 해임 요청일때 취소
    if me != study.user or me == person:
        print('Error: 잘못된 접근!')
        return redirect('studies:mainboard', study_pk)
    
    studying = Studying.objects.get(study=study, user=person)
    studying.permission = 1
    
    return redirect('studies:mainboard', study_pk)


def condition(request, study_pk: int, condition_num: int):
    study = get_object_or_404(Study, pk=study_pk)

    # 스터디 장만 변경 가능
    if request.user != study.user:
        return redirect('studies:mainboard', study_pk)
    
    if request.method == 'POST':
        if condition_num in [1, 2, 3]:
            study.join_condition = condition_num

            if study.join_condition == 3:
                study.is_recruiting = 2
            elif Studying.objects.filter(study=study).aggregate(cnt=Count('*'))['cnt'] < study.capacity and study.join_condition != 3 and study.is_recruiting == 2:
                study.is_recruiting = 1
            elif Studying.objects.filter(study=study).aggregate(cnt=Count('*'))['cnt'] == study.capacity and study.join_condition != 3 and study.is_recruiting == 1:
                study.is_recruiting = 2
                
            study.save()
            return redirect('studies:mainboard', study_pk)
        else:
            print('올바르지 않은 조건 번호입니다.')
            return redirect('studies:mainboard', study_pk)
    else:
        print('잘못된 요청입니다.')
        return redirect('studies:mainboard', study_pk)
