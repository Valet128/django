from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    def image_path(instance, filename):
        return '/'.join(['users', str(instance.id), filename])

    photo = models.ImageField(upload_to=image_path, blank=True, null=True, verbose_name="Фотография")
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name="Номер телефона")

    