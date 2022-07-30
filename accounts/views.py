from email import message
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import ProfileForm, SingupForm, PasswordChangeForm
from django.contrib.auth.views import (
    LoginView, logout_then_login, 
    PasswordChangeView as AuthPasswordChangeView,
)
from .models import User


login = LoginView.as_view(template_name="accounts/login_form.html")

def logout(request):
    messages.success(request, '로그아웃 되었습니다.')
    return logout_then_login(request)

def signup(request):
    if request.method == 'POST':
        form = SingupForm(request.POST, request.FILES)
        if form.is_valid():
            signed_user = form.save()
            auth_login(request, signed_user)
            messages.success(request, "회원가입을 환영합니다.")
            # signed_user.send_welcome_email()  # FiX: 비동기 혹은 celery로 처리 필요
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
    else:
        form = SingupForm()

    return render(request, 'accounts/signup_form.html', {
        'form': form,
    })

@login_required
def profile_edit(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "프로필을 수정/저장했습니다.")
            return redirect("accounts:profile_edit")
    else:
        form = ProfileForm(instance=request.user)
    return render(request, "accounts/profile_edit_form.html", {
        "form": form,
    })


class PasswordChangeView(LoginRequiredMixin, AuthPasswordChangeView):
    success_url = reverse_lazy("accounts:password_change")
    template_name = 'accounts/password_change_form.html'
    form_class = PasswordChangeForm
    
    def form_valid(self, form):
        messages.success(self.request, "암호를 변경했습니다.")
        return super().form_valid(form)


password_change = PasswordChangeView.as_view()

@login_required
def user_follow(request, username):
    follow_user = get_object_or_404(User, username=username, is_active=True)
    request.user.following_set.add(follow_user)
    follow_user.follower_set.add(request.user)
    # request.user => follow_user를 팔로우할려고 합니다.
    messages.success(request, f"{follow_user}님을 팔로우했습니다.")
    redirect_url = request.META.get("HTTP_REFERER", "root")
    return redirect(redirect_url)

@login_required
def user_unfollow(request, username):
    unfollow_user = get_object_or_404(User, username=username, is_active=True)
    request.user.following_set.remove(unfollow_user)
    unfollow_user.follower_set.remove(request.user)
    messages.success(request, f"{unfollow_user}님을 언팔했습니다.")
    redirect_url = request.META.get("HTTP_REFERER", "root")
    return redirect(redirect_url)