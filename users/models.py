from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .managers import CustomUserManager


class Survey(models.Model):
    is_accepted = models.BooleanField(default=False)
    rate = models.IntegerField(default = 0)
    review = models.TextField(max_length = 5000, default = 'Пустой отзыв')


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    name = models.CharField(max_length=30)
    is_renter = models.BooleanField(default=True)
    is_landlord = models.BooleanField(default=False)
    is_moderator = models.BooleanField(default=False)
    is_first = models.BooleanField(default=True)
    surveys = models.ManyToManyField(Survey)
    clients = models.ManyToManyField('self') #landlords for renter, renters for landlords
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
    def __str__(self):
        return self.email



class Message(models.Model):
    author = models.CharField(max_length = 50)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

    def getTime(self):
        return {
            'year': self.timestamp.year,
            'month':self.timestamp.month,
            'day': self.timestamp.day,
            'hours': self.timestamp.hour,
            'minutes': self.timestamp.minute,
        }


class Chat3(models.Model):
    name = models.TextField(max_length = 100)
    messages = models.ManyToManyField(Message, blank = True, default = None)
    landlord = models.OneToOneField(CustomUser, primary_key = True, on_delete = models.CASCADE)
    users = models.ManyToManyField(CustomUser, related_name="chat_users")

    def __str__(self):
        return self.name  

class Problem(models.Model):
    is_checked = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length = 5000, default = 'Описание проблемы')