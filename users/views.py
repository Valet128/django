from django.contrib.auth.views import PasswordChangeView, PasswordResetConfirmView, PasswordResetView
from django.views.generic import FormView, DetailView
from store.utils import DataMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CustomAuthenticationForm, UserPasswordChangeForm, UserPasswordResetForm, UserPasswordResetConfirmForm
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate

from django.shortcuts import redirect
from users.models import CustomUser



class LoginUser(DataMixin, FormView):
    form_class = CustomAuthenticationForm
    template_name = 'users/login.html'
    title = "Авторизация"
    success_url = reverse_lazy('users:profile')

    def get(self, request):
        if request.user.is_authenticated:
                return redirect('users:profile')
        return self.render_to_response(self.get_context_data())

    def form_valid(self, form):
        
        if form.is_valid():
            user_auth = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user_auth is not None:
                login(self.request, user_auth)
                return redirect('users:profile')

        return super().form_valid(form)
    
class RecallView(LoginRequiredMixin, DataMixin, DetailView):
    model = CustomUser
    template_name = 'users/recall.html'
    title = "Удаление аккаунта"
    
    def get_success_url(self):
        return reverse_lazy('users:recall')
    
    def get_object(self, queryset=None):
        return self.request.user
    
    def post(self, request):
        user = request.user
        user.delete()
        return redirect('/')

class ProfileUser(LoginRequiredMixin, DataMixin, DetailView):
    model = CustomUser
    template_name = 'users/profile.html'
    title = "Профиль пользователя"

    def get_success_url(self):
        return reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordChange(LoginRequiredMixin, DataMixin, PasswordChangeView):
    form_class =  UserPasswordChangeForm
    success_url = reverse_lazy('users:password_change_done')
    template_name = 'users/password_change_form.html'
    title = 'Смена пароля'


class UserPasswordReset(DataMixin, PasswordResetView):
    form_class = UserPasswordResetForm
    template_name='users/password_reset_form.html'
    email_template_name='users/password_reset_email.html'
    success_url=reverse_lazy('users:password_reset_done')
    title = "Сброс пароля"


class UserPasswordResetConfirm(DataMixin, PasswordResetConfirmView):
    form_class = UserPasswordResetConfirmForm
    template_name='users/password_reset_confirm.html'
    success_url=reverse_lazy('users:password_reset_complete')
    title = "Новый пароль"
