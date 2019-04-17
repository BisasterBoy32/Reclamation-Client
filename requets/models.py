from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Requet(models.Model):

    client = models.ForeignKey(User , on_delete = models.CASCADE , related_name = "requets")
    content = models.TextField()
    state = models.CharField(max_length = 100 , default="ont étape de traitement")
    tech = models.ForeignKey(User , on_delete = models.CASCADE , null = True , related_name = "works")
    pub_date = models.DateTimeField(default = timezone.now())
    aprove_date = models.DateTimeField(null = True)

    def __str__(self):
        if len(self.content) > 100 :
            return self.content[0:100] + "..."
        else :
            return self.content

    def aprove(self):
        self.aprove_date = timezone.now()
        tech = User.objects.filter(profile__group == "tech").order_by("works").first()
        self.tech = tech

    def summary(self):
        if len(self.content) > 100 :
            return self.content[0:100] + "..."
        else :
            return self.content

    def Requet_fixed(self):
        return self.state == "solved"
