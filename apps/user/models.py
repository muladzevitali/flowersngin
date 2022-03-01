from django.contrib.auth.models import (AbstractUser, PermissionsMixin, BaseUserManager)
from django.db import models
from model_utils.models import TimeStampedModel


class UserManager(BaseUserManager):
    use_in_migration = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The Email address must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser, PermissionsMixin):
    DEFAULT_TIMEZONE = "UTC+4"

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    timezone = models.CharField(default=DEFAULT_TIMEZONE, max_length=10)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __repr__(self):
        return f"User({self.id})"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


class Contact(TimeStampedModel):
    class SubjectChoices(models.TextChoices):
        ORDER = 'Ik heb een vraag over mijn bestelling'
        RECIPE = 'Ik heb een eigen recept'
        OTHER = 'Andere'

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=50)
    email = models.EmailField()
    subject = models.CharField(choices=SubjectChoices.choices, max_length=200)
    text = models.TextField()

    def __str__(self):
        return f'Contact({self.id})'
