from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email=None, password=None, **extra_fields):
        if not email:
            raise ValueError("Kindly enter an email address for this user.")

        # create the user, using the given email and password
        user = self.model(
            email=self.normalize_email(email.lower()),
            username=self.normalize_email(email.lower()),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, password=None, **extra_fields):
        if password is None:
            raise ValueError("Kindly enter a valid password for this superuser.")

        # create the superuser, using the given email and password
        user = self.create_user(email, password)
        user.is_superuser = user.is_staff = True
        user.save()
        return user


class CustomUser(AbstractUser, PermissionsMixin):
    USER_TYPES = [
        ('user', ('User')),
        ('admin', ('Admin'))
    ]
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    user_type = models.CharField(max_length=10, choices=USER_TYPES, null=True, blank=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

