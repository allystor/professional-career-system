from django.db import models
from .forms.choices import *
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('Usuários devem ter um endereço de e-mail válido.')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(
            username=username,
            email=email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class UserAutentication(models.Model):
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(verbose_name='E-mail', unique=True)
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.email
    
    @property
    def is_anonymous(self):
        return not self.is_authenticated

    @property
    def is_authenticated(self):
        return self.is_active
    
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

"""class Oportunity(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    area = models.CharField(max_length=100, choices=AREA_CHOICES)
    salary = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    type = models.CharField(max_length=100, choices=TYPE_CHOICES)
    level = models.CharField(max_length=100, choices=LEVEL_CHOICES)
    requirements = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title"""