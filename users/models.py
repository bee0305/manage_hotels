from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser

from .managers import CustomUserManager

class User(AbstractUser):
    """ 
    username + email for signup; email for login;
    user should choose at the moment of signUp one of two options: 
    hotel_manager can crud objects of hotels
    """
    username = models.CharField(_("Username"), unique=True, max_length=120)
    email = models.EmailField(_("Email"), unique=True)
    is_hotel_manager = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        return self.username
