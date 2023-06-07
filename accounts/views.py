from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from .forms import CustomUserCreationForm, CustomAuthenticationFormForm, CustomUserChangeForm, CustomPasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

# Create your views here.


# 테스트용 index입니다
def index(request):
    return render(request, 'accounts/index.html')


def signup(request):
    if request.user.is_authenticated:
        return redirect('studies:index')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend',)
            
            prev_url = request.session.get('prev_url')
            # 이전 페이지의 URL 정보가 있으면 해당 URL로 리다이렉트합니다.
            if prev_url:
                # 이전 페이지의 URL 정보를 삭제합니다.
                del request.session['prev_url']
                return redirect(prev_url)
            
            return redirect('main')
    else:
        form = CustomUserCreationForm()
        
    # prev_url에 회원가입 페이지로 이동하기 이전 페이지 정보 기록 
    request.session['prev_url'] = request.META.get('HTTP_REFERER')
    
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)


def login(request):
    if request.user.is_authenticated:
        return redirect('studies:index')
    
    if request.method == 'POST':
        form = CustomAuthenticationFormForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            
            prev_url = request.session.get('prev_url')
            if prev_url:
                del request.session['prev_url']
                return redirect(prev_url)
            
            return redirect('main')
    else:
        form = CustomAuthenticationFormForm()
    
    request.session['prev_url'] = request.META.get('HTTP_REFERER')
    
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)


@login_required
def logout(request):
    auth_logout(request)
    
    # 작업 성공 후 이전 페이지로 이동
    prev_url = request.META.get('HTTP_REFERER')
    if prev_url:
        # 현재 프로필 페이지에 있다면 메인페이지로 이동
        if '/profile/' in prev_url:
            return redirect('main')
        return redirect(prev_url)
        
    return redirect('main')


@login_required
def delete(request):
    request.user.delete()
    auth_logout(request)
    
    return redirect('main')


@login_required
def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('main')
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/update.html', context)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            
            return redirect('main')
    else:
        form = CustomPasswordChangeForm(request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/change_password.html', context)


def profile(request, username):
    user = get_user_model()
    person = user.objects.get(username=username)
    context = {
        'person': person
    }
    return render(request, 'accounts/profile.html', context)