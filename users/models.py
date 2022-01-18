from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser


# aqsfrom .managers import CustomUserManager
from city.models import City


class User(AbstractUser):
    """ 
    username + email for signup; email for login;    
    hotel_manager can crud objects of hotels
    """
    username = models.CharField(_("Username"), unique=True, max_length=120)
    email = models.EmailField(_("Email"), unique=True)
    is_hotel_manager = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    # objects = CustomUserManager()

    def __str__(self):
        return self.username


class HotelManager(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='hotel_manager')
    city = models.ForeignKey(City,related_name='managers',
                            on_delete=models.SET_NULL,null=True)


    def __str__(self) -> str:
        return self.user.username

 


# @receiver(post_save, sender=HotelManager)
# def update_stock(sender, instance, **kwargs):
#     instance.user.is_hotel_manager = True
#     instance.user.is_hotel_manager.save()