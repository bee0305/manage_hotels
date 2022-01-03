from django.db.models.signals import post_save
from django.dispatch import receiver
# from django.contrib.auth import get_user_model
from users.models import HotelManager

def create_manager(sender,instance,created,*args,**kwargs):
    if created:
        print('creating manager')
        instance.user.is_hotel_manager = True

post_save.connect(create_manager,sender=HotelManager)