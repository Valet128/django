from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(email, password, **extra_fields)
    
class CustomUser(AbstractBaseUser, PermissionsMixin):
   
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now, verbose_name="Дата и время")

    last_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="Фамилия")
    first_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="Имя")
    middle_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="Отчество")
    email = models.EmailField(unique=True, blank=True, null=True, verbose_name="Эл. адрес")
    password = models.CharField(max_length=200, blank=True, null=True, verbose_name="Пароль")
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name="Номер телефона")
    address = models.TextField(max_length=1000, blank=True, null=True, verbose_name="Адрес")
    ip_address = models.CharField(max_length=15, blank=True, null=True, verbose_name="Ip-адрес")
    
    personal_data_accepted = models.BooleanField(verbose_name="Согласие на обработку персональных данных", blank=True, null=True)
    personal_data_transfer_accepted = models.BooleanField(verbose_name="Согласие на передачу персональных данных третьим лицам", blank=True, null=True)
    send_messages_accepted = models.BooleanField(verbose_name="Согласие на получение рекламных и информационных сообщений", blank=True, null=True)
    users_agreement_accepted = models.BooleanField(verbose_name="Согласие на условия пользовательского соглашения", blank=True, null=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    objects = CustomUserManager()

    USERNAME_FIELD = 'email' # Поле для аутентификации (вместо username)
    REQUIRED_FIELDS = [] # Дополнительные обязательные поля

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.email

    def get_short_name(self):
        return self.first_name or self.email

