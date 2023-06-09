import json
import operator
import logging
from functools import reduce

from django.http import JsonResponse, Http404, QueryDict, HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods

# from rest_framework import status
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response

from taggit.models import Tag

from .forms import ProblemForm, ReviewForm, CommentForm
from .models import Problem, Review, Comment
# from .serializers import CommentSerializer

from studies.models import Study


# 로깅 설정
logger = logging.getLogger(__name__)


# Create your views here.
@login_required
def detail(request, pk):
    '''
    - ✅ Problem, Review, Comment에 달린 모든 태그를 모아보는 기능
    '''
    problem = get_object_or_404(
        Problem.objects.prefetch_related(
            'tags',
            'review_set__comment_set__tags',
            'review_set__tags',
        ).select_related('study'),
        pk=pk
    )

    if not problem.study.studying_users.filter(username=request.user).exists():
        return redirect('studies:detail', problem.study.pk)
    
    querydict = {
        'problem': Q(problem_set=pk),
        'review': Q(review_set__in=problem.review_set.values('id')),
        'comment': Q(comment_set__in=Comment.objects.filter(review__in=problem.review_set.all()).values('id'))
    }

    tags = Tag.objects.filter(reduce(operator.__or__, querydict.values()))
    tags = tags.annotate(freq=Count('name'))
    ordered_tags = tags.order_by('-freq').values('name')

    context = {
        'problem': problem,
        'tags': ordered_tags.values(),
        'comment_form': CommentForm(),
    }
    return render(request, 'reviews/detail.html', context)


@login_required
def create(request):
    study_id = request.GET.get('study', request.session.get('study_id'))
    member = get_object_or_404(
        Study, pk=study_id,
    ).studying_users.filter(username=request.user).exists()
    
    if study_id is None or not member:
        return redirect('studies:detail', study_id)
    
    request.session['study_id'] = study_id
    
    if request.method == 'POST':
        form = ProblemForm(data=request.POST)
        if form.is_valid():
            problem = form.save(commit=False)
            problem.user, problem.study = request.user, get_object_or_404(Study, pk=study_id)
            problem.save()
            form.save_m2m()
            return redirect('reviews:detail', problem.pk)

        return redirect('studies:mainboard', study_id)
    else:
        form = ProblemForm()
    context = {
        'form': form,
    }
    return render(request, 'reviews/create.html', context)


@login_required
def update(request, pk):
    problem = get_object_or_404(Problem.objects.select_related('study'), pk=pk)
    
    # reviews:detail에서 studies:detail로 가는 코드가 있지만,
    # 네트워크 비용 감소를 위해 바로 studies:detail로 가도록 작성
    if not problem.study.studying_users.filter(username=request.user).exists():
        return redirect('studies:detail', problem.study.pk)
    
    if request.user != problem.user:
        return redirect('reviews:detail', problem.pk)
    
    if request.method == 'POST':
        form = ProblemForm(data=request.POST, instance=problem)
        if form.is_valid():
            updated_form = form.save(commit=False)
            updated_form.save()
            form.save_m2m()
            return redirect('reviews:detail', problem.pk)
    else:
        form = ProblemForm(instance=problem)
    context = {
        'form': form,
    }
    return render(request, 'reviews/update.html', context)


@login_required
def delete(request, pk):
    problem = get_object_or_404(
        Problem.objects.select_related('study'), pk=pk,
    )
    if not problem.study.studying_users.filter(username=request.user).exists():
        return redirect('studies:detail', problem.study.pk)

    if request.user == problem.user:
        problem.delete()
        return redirect('studies:mainboard', problem.study.pk)
    return redirect('reviews:detail', pk)
    

@login_required
def review_create(request, pk):
    problem = get_object_or_404(
        Problem.objects.select_related('study'),
        pk=pk,
    )
    
    if not problem.study.studying_users.filter(username=request.user).exists():
        return redirect('studies:detail', problem.study.pk)
    
    if request.method == 'POST':
        form = ReviewForm(data=request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user, review.problem = request.user, problem
            review.save()
            form.save_m2m()
            context = {
                'problem': Problem.objects.get(pk=pk)
            }
            return render(request, 'reviews/reviews.html', context)
    else:
        form = ReviewForm()
    context = {
        'form': form,
        'problem_pk': pk,
    }
    return render(request, 'reviews/review_create.html', context)


@login_required
def review_update(request, review_pk):
    review = get_object_or_404(
        Review.objects.select_related('problem__study'),
        pk=review_pk,
    )
    
    if not review.problem.study.studying_users.filter(username=request.user).exists():
        return redirect('studies:detail', review.problem.study.pk)
    
    if request.user != review.user:
        return redirect('reviews:detail', review.problem.pk)
    
    if request.method == 'POST':
        form = ReviewForm(data=request.POST, instance=review)
        if form.is_valid():
            review = form.save(commit=False)
            review.save()
            form.save_m2m()
            return redirect('reviews:detail', review.problem.pk)
    else:
        form = ReviewForm(instance=review)
    context = {
        'form': form,
    }
    return render(request, 'reviews/review_update.html', context)


@login_required
def review_delete(request, review_pk):
    review = get_object_or_404(
        Review.objects.select_related('problem__study'),
        pk=review_pk
    )
    if not review.problem.study.studying_users.filter(username=request.user).exists():
        return redirect('studies:detail', review.problem.study.pk)
    
    if request.user == review.user:
        review.delete()
        return redirect('studies:index')
    return redirect('reviews:detail', review.problem.pk)


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def comment_create(request, review_pk):
#     try:
#         review = get_object_or_404(
#             Review.objects.select_related('problem__study'),
#             pk=review_pk
#         )

#         if review is None:
#             logger.error(f"No Review found with pk: {review_pk}")
#             return Response({"error": "No Review found."}, status=status.HTTP_404_NOT_FOUND)
        
#         serializer = CommentSerializer(data=request.data, context={'review': review, 'user': request.user})

#         if not serializer.is_valid():
#             logger.error(f"Serializer validation failed with errors: {serializer.errors}")
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

#     except Exception as e:
#         logger.error(f"Unexpected error occurred: {e}")
#         return Response({"error": "Unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@login_required
def comment_create(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user, comment.review = request.user, review
            comment.save()
            context = {
                'review': review,
            }
            return render(request, 'reviews/comments/list.html', context)
        return render(request, 'reviews/components/comment_create_not_valid.html')   # 작성 필요
    else:
        form = CommentForm()
    context = {
        'comment_form': form,
        'review': review,
    }
    return render(request, 'reviews/comments/create.html', context)


@require_http_methods(['GET', 'PUT'])
@login_required
def comment_update(request, comment_pk):
    comment = get_object_or_404(
        Comment.objects.select_related('review'),
        pk=comment_pk
    )
    context = {
        'comment': comment,
    }    
    if request.user != comment.user:
        return render(request, 'reviews/comments/item.html', context)
    
    if request.method == 'PUT':
        data = QueryDict(request.body).dict()
        form = CommentForm(data=data, instance=comment)
        if form.is_valid():
            form.save()
            return render(request, 'reviews/comments/item.html', context)
        context['comment_form'] = form
    else:
        context['comment_form'] = CommentForm(instance=comment)
    return render(request, 'reviews/comments/update.html', context)


@require_http_methods(['DELETE'])
@login_required
def comment_delete(request, comment_pk):
    comment = get_object_or_404(
        Comment.objects.select_related('review'),
        pk=comment_pk
    )
    context = {
        'review': comment.review
    }
    if request.user == comment.user:
        comment.delete()
        return HttpResponse()
    return render(request, 'reviews/comments/item.html', context)

    
@login_required
def like(request):
    try:
        data = json.loads(request.body)
    except:
        raise Http404("Request not valid")
    
    object_identifier = data.get('objectIdentifier')
    if object_identifier is not None:
        model, pk = object_identifier.split('-')
        if model not in {'Problem', 'Review', 'Comment'}:
            raise Http404("Request not valid")
        obj = get_object_or_404(eval(model), pk=pk)

    # 조건문 추가해 Problem, Review, Comment 별로 swap_text 수정 가능
    if request.user in obj.like_users.all():
        obj.like_users.remove(request.user)
        response = {
            'swap_text': '좋아요',
        }
    else:
        obj.like_users.add(request.user)
        response = {
            'swap_text': '좋아요 취소',
        }
    return JsonResponse(response)
