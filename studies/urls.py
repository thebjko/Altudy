from django.urls import path
from . import views


app_name = 'studies'
urlpatterns = [
    # 스터디 CRUD
    path('', views.index, name='index'),
    path('<int:study_pk>/', views.detail, name='detail'),
    path('create/', views.create, name='create'),
    path('<int:study_pk>/delete/', views.delete, name='delete'),
    path('<int:study_pk>/update/', views.update, name='update'),
    # 스터디 join_conditoin 변경
    path('<int:study_pk>/condition/<int:condition_num>/', views.condition, name='condition'),
    
    # 스터디 가입 요청 관련 {POST}
    path('<int:study_pk>/join/', views.join, name='join'), # 스터디 가입, 가입 요청
    path('<int:study_pk>/withdraw/', views.withdraw, name='withdraw'), # 스터디 탈퇴
    path('<int:study_pk>/accept/<username>/', views.accept, name='accept'), # 스터디 가입 요청 수락
    path('<int:study_pk>/reject/<username>/', views.reject, name='reject'), # 스터디 가입 요청 거절
    path('<int:study_pk>/expel/<username>/', views.expel, name='expel'), # 스터디원 방출
    path('<int:study_pk>/cancel/', views.cancel, name='cancel'), # 스터디 가입 요청 취소
  
    # 메인보드
    path('<int:study_pk>/mainboard/', views.mainboard, name='mainboard'),
    path('<int:study_pk>/mainboard/member/', views.member, name='member'),
    path('<int:study_pk>/mainboard/problem/', views.problem, name='problem'),
    path('<int:study_pk>/mainboard/problem/search/', views.problem_search, name='problem_search'),

    # 스터디 공지 in 메인보드
    path('<int:study_pk>/mainboard/announcement/', views.announcement, name='announcement'),
    path('<int:study_pk>/mainboard/announcement/create/', views.announcement_create, name='announcement_create'),
    path('<int:study_pk>/mainboard/announcement/<int:announcement_pk>/', views.announcement_detail, name='announcement_detail'),
    path('<int:study_pk>/mainboard/announcement/<int:announcement_pk>/update/', views.announcement_update, name='announcement_update'),
    path('<int:study_pk>/mainboard/announcement/<int:announcement_pk>/delete/', views.announcement_delete, name='announcement_delete'),
    
    # 스터디장 (Studying.permission) 임명(appoint), 해임(dismiss)
    # 부스터디장?
    path('<int:study_pk>/appoint/<username>/<int:permission>/', views.appoint, name='appoint'),
    path('<int:study_pk>/dismiss/<username>/', views.dismiss, name='dismiss'),
    
    # 스터디 댓글
    path('<int:study_pk>/comment/create/', views.comment_create, name='comment_create'),
    path('<int:study_pk>/comment/<int:comment_pk>/delete/', views.comment_delete, name='comment_delete'),
    path('<int:study_pk>/comment/<int:comment_pk>/update/', views.comment_update, name='comment_update'),
]