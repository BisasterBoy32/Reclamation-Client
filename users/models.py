from django.db import models
from django.contrib.auth.models import User
from requets.models import Requet


# Create your models here.

class Profile(models.Model):
    owner = models.OneToOneField(User ,on_delete = models.CASCADE)
    location = models.CharField(max_length = 100)
    phone_number = models.CharField(max_length = 100,null = True)
    group = models.CharField(max_length = 100 , default = "client")
    type = models.CharField(max_length = 100 ,null = True)

    def __str__(self):
        return self.owner.username

    def count_client(self):
        clients = Profile.objects.filter(group = "client").count()
        return clients


    def count_tech(self):
        techs = Profile.objects.filter(group = "tech").count()
        return techs

    def count_entreprise(self):
        entreprise = Profile.objects.filter(type = "entreprise").count()
        return entreprise

    def count_personne(self):
        personne = Profile.objects.filter(type = "personne").count()
        return personne

    def count_requets(self):
        return Requet.objects.count()

    def count_fixed_requets(self):
        return Requet.objects.filter(state = "Problème Résolu").count()

    def count_approved_requets(self):
        return Requet.objects.filter(state = "apprové par l'administrateur").count()

    def count_new_requets(self):
        return Requet.objects.filter(state = "ont étape de traitement").count()





class Personne(models.Model):
    profile = models.OneToOneField(Profile , on_delete = models.CASCADE )
    first_name = models.CharField(max_length = 256)
    last_name = models.CharField(max_length = 256 )

class Company(models.Model):
    profile = models.OneToOneField(Profile , on_delete = models.CASCADE )
    name = models.CharField(max_length = 256)
