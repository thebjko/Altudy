from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        user = sociallogin.user
        if not user.email:
            # 로그인된 소셜 계정의 이메일이 없을 경우에만 자동으로 채워넣음
            user.email = sociallogin.account.extra_data['email']
        if sociallogin.account.provider == 'google':
            # 구글 로그인인 경우 이메일의 아이디 부분을 유저네임으로
            email_id = sociallogin.account.extra_data['email'].split('@')[0]
            user.username = email_id