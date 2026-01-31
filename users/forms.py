from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth import get_user_model, password_validation
import uuid

User = get_user_model()

class CourseCustomUserCreationForm(UserCreationForm):
    full_uuid = uuid.uuid4()
    uuid_hex =full_uuid.hex

    password = uuid_hex[:8]
    
    amount = forms.DecimalField(max_digits=10, label="Сумма", widget=forms.TextInput(attrs={'class': 'form-item__text'}))
    product_name = forms.CharField(max_length=255, label="Название курса", widget=forms.TextInput(attrs={'class': 'form-item__text'}))
    customer_firstname = forms.CharField(max_length=100, min_length=2, label="Ваше Имя", widget=forms.TextInput(attrs={'class': 'form-item__text'}))
    email = forms.EmailField(label="Эл. почта", widget=forms.EmailInput(attrs={'class': 'form-item__text'}))
    customer_phone = forms.CharField(max_length=20, min_length=7, label="Номер телефона", widget=forms.TextInput(attrs={'class': 'form-item__text'}))
    
    personal_data_accepted = forms.BooleanField(initial=False, widget=forms.CheckboxInput(attrs={'class': 'form-item__text'}))
    personal_data_transfer_accepted = forms.BooleanField(initial=False, widget=forms.CheckboxInput(attrs={'class': 'form-item__text'}))
    send_messages_accepted = forms.BooleanField(initial=False, widget=forms.CheckboxInput(attrs={'class': 'form-item__text'}))
    users_agreement_accepted = forms.BooleanField(initial=False, widget=forms.CheckboxInput(attrs={'class': 'form-item__text'}))

    password1 = forms.CharField(label='',
    widget=forms.HiddenInput(attrs={'class': 'label-none', 'placeholder': 'Пароль'}),
    initial=password
    )

    password2 = forms.CharField(label='',
    widget=forms.HiddenInput(attrs={'class': 'label-none', 'placeholder': 'Подтверждение пароля'}),
    initial=password
    )

    class Meta:
        model = User
        fields = ('email',)


    def clean(self):
        self._validate_unique = False
        return self.cleaned_data    

    

class BookCustomUserCreationForm(UserCreationForm):
    full_uuid = uuid.uuid4()
    uuid_hex =full_uuid.hex

    password = uuid_hex[:8]

    product_name = forms.CharField(max_length=255, label="Название курса", widget=forms.TextInput(attrs={'class': 'form-item__text'}))
    amount = forms.DecimalField(max_digits=10, label="Сумма", widget=forms.TextInput(attrs={'class': 'form-item__text'}))
    
    email = forms.EmailField(label="Эл. почта", widget=forms.EmailInput(attrs={'class': 'form-item__text'}))
    customer_phone = forms.CharField(max_length=20, min_length=7, label="Номер телефона", widget=forms.TextInput(attrs={'class': 'form-item__text'}))

    #Данные для доставки
    customer_lastname = forms.CharField(max_length=100, min_length=2, label="Ваша Фамилия", widget=forms.TextInput(attrs={'class': 'form-item__text'}))
    customer_firstname = forms.CharField(max_length=100, min_length=2, label="Ваше Имя", widget=forms.TextInput(attrs={'class': 'form-item__text'}))
    customer_middlename = forms.CharField(max_length=100, min_length=2, label="Ваше Отчество", widget=forms.TextInput(attrs={'class': 'form-item__text'}))

    customer_address = forms.CharField(
        max_length=300, 
        min_length=2, 
        label="""Адрес доставки (Cтрана, 
регион (например, область, край, республика), 
город или населенный пункт,
улицу, номер дома и корпус (если есть),
квартиру или офис,
почтовый индекс.)""", 
        widget=forms.Textarea(
            attrs={
                'class': 'form-item__text', 
                'placeholder': 'Cтрана, Регион, Город, Улица, Квартира, Индекс'
                }))

    personal_data_accepted = forms.BooleanField(initial=False, widget=forms.CheckboxInput(attrs={'class': 'form-item__text'}))
    personal_data_transfer_accepted = forms.BooleanField(initial=False, widget=forms.CheckboxInput(attrs={'class': 'form-item__text'}))
    send_messages_accepted = forms.BooleanField(initial=False, widget=forms.CheckboxInput(attrs={'class': 'form-item__text'}))
    users_agreement_accepted = forms.BooleanField(initial=False, widget=forms.CheckboxInput(attrs={'class': 'form-item__text'}))


    password1 = forms.CharField(
    widget=forms.HiddenInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}),
    initial=password
    )

    password2 = forms.CharField(
    widget=forms.HiddenInput(attrs={'class': 'form-control', 'placeholder': 'Подтверждение пароля'}),
    initial=password
    )

    class Meta:
        model = User
        fields = ('email', )
        
    def clean(self):
        self._validate_unique = False
        return self.cleaned_data
    
class FreeEventCustomUserCreationForm(UserCreationForm):
    full_uuid = uuid.uuid4()
    uuid_hex = full_uuid.hex

    password = uuid_hex[:8]
    
    product_name = forms.CharField(max_length=255, label="Название курса", widget=forms.TextInput(attrs={'class': 'form-item__text'}))
    customer_firstname = forms.CharField(max_length=100, min_length=2, label="Ваше Имя", widget=forms.TextInput(attrs={'class': 'form-item__text'}))
    email = forms.EmailField(label="Эл. почта", widget=forms.EmailInput(attrs={'class': 'form-item__text'}))
    customer_phone = forms.CharField(max_length=20, min_length=7, label="Номер телефона", widget=forms.TextInput(attrs={'class': 'form-item__text'}))
    personal_data_accepted = forms.BooleanField(initial=False, widget=forms.CheckboxInput(attrs={'class': 'form-item__text'}))
    personal_data_transfer_accepted = forms.BooleanField(initial=False, widget=forms.CheckboxInput(attrs={'class': 'form-item__text'}))
    send_messages_accepted = forms.BooleanField(initial=False, widget=forms.CheckboxInput(attrs={'class': 'form-item__text'}))
    users_agreement_accepted = forms.BooleanField(initial=False, widget=forms.CheckboxInput(attrs={'class': 'form-item__text'}))

    password1 = forms.CharField(label='',
    widget=forms.HiddenInput(attrs={'class': 'label-none', 'placeholder': 'Пароль'}),
    initial=password
    )

    password2 = forms.CharField(label='',
    widget=forms.HiddenInput(attrs={'class': 'label-none', 'placeholder': 'Подтверждение пароля'}),
    initial=password
    )

    class Meta:
        model = User
        fields = ('email',)


    def clean(self):
        self._validate_unique = False
        return self.cleaned_data    

class CustomAuthenticationForm(AuthenticationForm):
    """Форма для аутентификации пользователей"""
    username = forms.CharField(label='Эл. адрес', widget=forms.EmailInput(attrs={'class': 'form-item__text'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-item__text'}))
    


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
    
   