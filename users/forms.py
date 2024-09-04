from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth import get_user_model, password_validation


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Эл. адрес', widget=forms.EmailInput(attrs={'class': 'form-item__text'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-item__text'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']

class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Эл. адрес', 
        widget=forms.EmailInput(attrs={'class': 'form-item__text'}),
        error_messages={'unique': 'Такой e-mail уже зарегистрирован.'}
        )
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-item__text'}))
    password2 = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput(attrs={'class': 'form-item__text'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'password1', 'password2', 'first_name']
        labels ={
            'first_name': 'Ваше имя',
            'phone': 'Номер телефона',
        }
        widgets ={
            'first_name': forms.TextInput(attrs={'class': 'form-item__text'}),
            # 'phone': forms.TextInput(attrs={'class': 'form-item__text'}),
        }

class ProfileUserForm(forms.ModelForm):
    username = forms.CharField(
        disabled=True, 
        label='Эл. адрес', 
        widget=forms.EmailInput(attrs={'class': 'form-item__text'})
        )
    first_name = forms.CharField(
        label='Ваше имя', 
        widget=forms.TextInput(attrs={'class': 'form-item__text'}),
        )
    phone = forms.CharField(
        label='Номер телефона', 
        widget=forms.TextInput(attrs={'class': 'form-item__text'}),
        )
    photo = forms.ImageField(
        label='Фотография', 
        widget=forms.FileInput(attrs={'class': 'form-item__text'}),
        )

    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'phone', 'photo']
        labels ={
            'first_name': 'Ваше имя',
        }
        widgets ={
            'first_name': forms.TextInput(attrs={'class': 'form-item__text'}),
            'phone': forms.TextInput(attrs={'class': 'form-item__text'}),
        }

class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='Старый пароль', widget=forms.PasswordInput(attrs={'class': 'form-item__text'}))
    new_password1 = forms.CharField(label='Новый пароль', widget=forms.PasswordInput(attrs={'class': 'form-item__text'}))
    new_password2 = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput(attrs={'class': 'form-item__text'}))

class UserPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label='Эл. адрес', widget=forms.EmailInput(attrs={'class': 'form-item__text'}))     
  
class UserPasswordResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=("Новый пароль"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 'class': 'form-item__text'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=("Подтвердите новый пароль"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 'class': 'form-item__text'}),
    )
    
   