from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    owner = models.OneToOneField(User ,on_delete = models.CASCADE)
    location = models.CharField(max_length = 100)
    group = models.CharField(max_length = 100 , default = "client")

    def __str__(self):
        return self.owner.username
