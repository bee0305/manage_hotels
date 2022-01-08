from django.db import models
from autoslug import AutoSlugField


class City(models.Model):
    # from api:  ['AMS', '"Amsterdam"']
    #            short_cut; name
    name = models.CharField(max_length=120, unique=True)
    city_code = models.CharField(max_length=24)
    slug = AutoSlugField(populate_from='name', unique=True)

    class Meta:
        verbose_name_plural = 'cities'    

    def __str__(self) -> str:
        return self.name


class Hotel(models.Model):
    # from api: "ANT";"ANT11";"Agora"
    #           short_cut;unid;name
    city_code = models.CharField(max_length=12)
    unid = models.CharField(max_length=24, unique=True)
    name = models.CharField(max_length=120)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='hotels')

    def save(self,*args,**kwargs):
        if not self.city_code:
            self.city_code = self.city.city_code
            print('model says:',self.city_code)
        super().save(*args,**kwargs)


    def __str__(self) -> str:
        return self.name
