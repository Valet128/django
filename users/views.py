from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetConfirmView, PasswordResetView
from django.views.generic import CreateView, UpdateView
from store.utils import DataMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import LoginUserForm, RegisterUserForm, ProfileUserForm, UserPasswordChangeForm, UserPasswordResetForm, UserPasswordResetConfirmForm
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    title = "Авторизация"


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    title = "Регистрация"
    success_url = reverse_lazy('users:login')
    
    def form_valid(self, form):
        title_message = 'Регистрация'
        text_message = f"""{form.cleaned_data['first_name']}, Вы зарегистрировались на сайте shvedovaav.ru!"""
        email_to = [form.cleaned_data['username']]

        email = EmailMessage(
            subject=title_message,
            body=text_message,
        to=email_to
        )
        email.send()
        return super().form_valid(form)


class ProfileUser(LoginRequiredMixin, DataMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
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
