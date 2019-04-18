from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    owner = models.OneToOneField(User ,on_delete = models.CASCADE)
    location = models.CharField(max_length = 100)
    phone_number = models.IntegerField(null = True)
    group = models.CharField(max_length = 100 , default = "client")
    type = models.CharField(max_length = 100 ,null = True)

    def __str__(self):
        return self.owner.username

    def count_client(self):
        clients = self.objects.filter(group = "client").count()
        return clients

    def count_tech(self):
        techs = self.objects.filter(group = "tech").count()
        return techs

    def count_entreprise(self):
        entreprise = self.objects.filter(type = "entreprise").count()
        return entreprise

    def count_personne(self):
        personne = self.objects.filter(type = "personne").count()
        return personne






class Personne(models.Model):
    profile = models.OneToOneField(Profile , on_delete = models.CASCADE )
    first_name = models.CharField(max_length = 256)
    last_name = models.CharField(max_length = 256 )

class Company(models.Model):
    profile = models.OneToOneField(Profile , on_delete = models.CASCADE )
    name = models.CharField(max_length = 256)
