from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    owner = models.OneToOneField(User ,on_delete = models.CASCADE)
    location = models.CharField(max_length = 100)
    phone_number = models.IntegerField(null = True)
    group = models.CharField(max_length = 100 , default = "client")
    type = models.CharField(max_length = 100 ,null = True)
    personne = models.OneToOneField(Personne ,on_delete = models.CASCADE ,null = True)
    company = models.OneToOneField(Commpany ,on_delete = models.CASCADE ,null = True)

    def __str__(self):
        return self.owner.username


class Personne(models.Model):
    first_name = models.CharField(max_length = 256)
    last_name = models.CharField(max_length = 256 )

class Company(models.Model):
    name = models.CharField(max_length = 256)
