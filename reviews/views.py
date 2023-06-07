import json
import operator
from functools import reduce

from django.http import JsonResponse, Http404
from django.contrib.auth.decorators import login_required
# from django.contrib.contenttypes.models import ContentType
from django.db.models import Count, Q
from django.shortcuts import render, get_object_or_404, redirect
# from rest_framework.decorators import api_view
from taggit.models import Tag, TaggedItem

# from .apps import ReviewsConfig
from .forms import ProblemForm, ReviewForm, CommentForm
from .models import Problem, Review, Comment
from studies.models import Study

'''다른 스터디 선택하기 기능이 추가되어야 한다'''
# Create your views here.
@login_required
def detail(request, pk):
    '''
    구현할 기능:
    - ✅ Problem, Review, Comment에 달린 모든 태그를 모아보는 기능
    - [ ] 클릭시 해당 태그가 사용된 Problem, Review, Comment로 이동하는 링크
    '''
    problem = get_object_or_404(
        Problem.objects.prefetch_related(
            'tags',
            'review_set__tags',
            'review_set__comment_set__tags',
        ),
        pk=pk
    )

    # querydict_for_content_type_id = {
    #     'current_app_label_query' : Q(app_label=ReviewsConfig.name),
    #     'model_name_query' : Q(model__in=['problem', 'review', 'comment'])
    # }

    # # used in content_type_query
    # query_for_content_type_id = reduce(operator.__and__, querydict_for_content_type_id.values())

    # # Query relevant content_type from TaggedItem model.    
    # content_type_query = Q(content_type_id__in=ContentType.objects.filter(query_for_content_type_id))

    # # Query relevant object_id from TaggedItem model.
    # object_query = Q(object_id=pk) | Q(object_id__in=problem.review_set.all())
    # for review in problem.review_set.all():
    #     object_query |= Q(object_id__in=review.comment_set.all())

    # tagged_items = TaggedItem.objects.filter(content_type_query&object_query)
    
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
    if study_id is None:
        return redirect('studies:index')
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
        # 'study_id': study_id,
    }
    return render(request, 'reviews/create.html', context)


@login_required
def update(request, pk):
    problem = get_object_or_404(Problem, pk=pk)
    if request.user != problem.user:
        return redirect('reviews:detail', problem.pk)
    
    if request.method == 'POST':
        form = ProblemForm(data=request.POST, instance=problem)
        if form.is_valid():
            form.save()
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
    problem = get_object_or_404(Problem, pk=pk)
    if request.user == problem.user:
        problem.delete()
        return redirect('studies:mainboard')
    # 권한이 없는 페이지 만들기?
    # 왔던 곳으로 되돌아가게 하려면?
    return redirect('reviews:detail', pk)
    

@login_required
def review_create(request, pk):
    problem = get_object_or_404(Problem, pk=pk)
    if request.method == 'POST':
        form = ReviewForm(data=request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user, review.problem = request.user, problem
            review.save()
            form.save_m2m()
            return redirect('reviews:detail', problem.pk)
    else:
        form = ReviewForm()
    context = {
        'form': form,
        'problem_pk': pk,
    }
    return render(request, 'reviews/review_create.html', context)


@login_required
def review_update(request, review_pk):
    review = get_object_or_404(Review.objects.select_related('problem'), pk=review_pk)
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
    review = get_object_or_404(Review.objects.select_related('problem'), pk=review_pk)
    if request.user == review.user:
        review.delete()
        return redirect('studies:index')
    return redirect('reviews:detail', review.problem.pk)


@login_required
def comment_create(request, review_pk):
    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            review = get_object_or_404(Review.objects.select_related('problem'), pk=review_pk)
            comment.user, comment.review = request.user, review
            comment.save()
            form.save_m2m()
            return redirect('reviews:detail', review.problem.pk)
    else:
        form = CommentForm()
    context = {
        'form': form,
    }
    return render(request, 'reviews/comment_create.html', context)


@login_required
def comment_update(request, comment_pk):
    comment = get_object_or_404(Comment.objects.select_related('review__problem'), pk=comment_pk)
    if request.user != comment.user:
        return redirect('reviews:detail', comment.review.problem.pk)
    
    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.save()
            form.save_m2m()
            return redirect('reviews:detail', comment.review.problem.pk)
    else:
        form = CommentForm()
    context = {
        'form': form,
    }
    return render(request, 'reviews/comment_create.html', context)


@login_required
def comment_delete(request, comment_pk):
    comment = get_object_or_404(Comment.objects.select_related('review__problem'), pk=comment_pk)
    if request.user == comment.user:
        comment.delete()
    return redirect('reviews:detail', comment.review.problem.pk)

    
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
        
    