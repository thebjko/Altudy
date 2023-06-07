from django.urls import path

from . import views


app_name = 'reviews'
urlpatterns = [
    path('<int:pk>/', views.detail, name='detail'),
    path('like/', views.like, name='like'),
    path('create/', views.create, name='create'),
    path('update/<int:pk>/', views.update, name='update'),
    path('delete/<int:pk>/', views.delete, name='delete'),
    path('review_create/<int:pk>/', views.review_create, name='review_create'),
    path('review_update/<int:review_pk>/', views.review_update, name='review_update'),
    path('review_delete/<int:review_pk>/', views.review_delete, name='review_delete'),
    path('comment_create/<int:review_pk>/', views.comment_create, name='comment_create'),
    path('comment_update/<int:comment_pk>/', views.comment_update, name='comment_update'),
    path('comment_delete/<int:comment_pk>/', views.comment_delete, name='comment_delete'),
]
