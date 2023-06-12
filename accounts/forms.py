from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import get_user_model


class CustomUserCreationForm(UserCreationForm):
    labels = {
        'username': '이름',
        'email': '이메일',
        'password1': '비밀번호',
        'password2': '비밀번호 확인',
    }

    username = forms.CharField(
        label='이름',
        widget=forms.TextInput(attrs={'class': 'my-custom-class'})
    )
    email = forms.EmailField(
        label='이메일',
        widget=forms.EmailInput(attrs={'class': 'my-custom-class'})
    )
    password1 = forms.CharField(
        label='비밀번호',
        widget=forms.PasswordInput(attrs={'class': 'my-custom-class'})
    )
    password2 = forms.CharField(
        label='비밀번호 확인',
        widget=forms.PasswordInput(attrs={'class': 'my-custom-class'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, label in self.labels.items():
            self.fields[field_name].label = label
            self.fields[field_name].help_text = ''
            self.fields[field_name].label_suffix = ''

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2',)


class CustomAuthenticationFormForm(AuthenticationForm):
    class Meta(AuthenticationForm):
        model = get_user_model()
        fields = ('username', 'password',)


class CustomUserChangeForm(UserChangeForm):
    labels = {
        'username': '이름',
        'email': '이메일',
    }

    username = forms.CharField(
        label='이름',
        widget=forms.TextInput(attrs={'class': 'my-custom-class'})
    )
    email = forms.EmailField(
        label='이메일',
        widget=forms.EmailInput(attrs={'class': 'my-custom-class'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].help_text = ''
            self.fields[field_name].label_suffix = ''
        self.fields['password'].help_text = ''

    class Meta(UserChangeForm):
        model = get_user_model()
        fields = ('username', 'email',)


class CustomPasswordChangeForm(PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].help_text = ''
            self.fields[field_name].label_suffix = ''

    class Meta(PasswordChangeForm):
        model = get_user_model()
        fields = ('old_password', 'new_password1', 'new_password2',)