from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, UserManager
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in
from datetime import datetime, timedelta

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'

    full_name = models.CharField(max_length=150)
    number = models.CharField(max_length=20, null=True, blank=True)
    university = models.CharField(max_length=150, null=True, blank=True)
    university_society = models.CharField(max_length=150, null=True, blank=True)
    university_society_position = models.CharField(max_length=150, null=True, blank=True,)
    year = models.IntegerField(default=1)
    streak = models.IntegerField(default=1)

    username = None

    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_first_name(self):
        try:
            return str(self.full_name).split(" ")[0]
        except:
            return str(self.full_name)

class LoginEvent(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )

    time_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user) + ": " + str(self.time_date)

def record_login_event(sender, user, request, **kwargs):
    login = LoginEvent.objects.create(
        user=user,
    )
    login.save()

    today = datetime.today().date()
    yesterday = today - timedelta(days=1)

    yesterdays_logins = LoginEvent.objects.filter(user=user, time_date__range=(yesterday, today))
    todays_logins = LoginEvent.objects.filter(user=user, time_date__range=(today, datetime.now()))
    if yesterdays_logins.exists():
        if not todays_logins.exists():
            user.streak = user.streak + 1
            user.save()
    else:
        user.streak = 1
        user.save()

user_logged_in.connect(record_login_event)