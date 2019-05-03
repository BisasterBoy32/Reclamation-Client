from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Count
from django.db.models import Q

# Create your models here.
class Requet(models.Model):

    client = models.ForeignKey(User , on_delete = models.CASCADE , related_name = "requets")
    problem = models.CharField(max_length = 256 , null = True)
    content = models.TextField()
    state = models.CharField(max_length = 100 , default="ont étape de traitement")
    tech = models.ForeignKey(User , on_delete = models.CASCADE , null = True , related_name = "works")
    pub_date = models.DateTimeField(default = timezone.now)
    aprove_date = models.DateTimeField(null = True)
    fix_date = models.DateTimeField(null = True)
    fix_confirm = models.BooleanField(default = False)

    def __str__(self):
        if len(self.content) > 100 :
            return self.content[0:100] + "..."
        else :
            return self.content
    def p_date(self):
        return self.pub_date.strftime("%m/%d/%Y, %H:%M")

    def aprove(self):
        self.aprove_date = timezone.now()
        requets_approveé = Count("works" ,filter = Q(works__state = "apprové par l'administrateur"))
        tech = User.objects.filter(
        profile__group = "tech" ,profile__address__region = self.client.profile.address.region
        ).annotate(requet_count = requets_approveé).order_by("requet_count").first()

        self.tech = tech
        self.state = "apprové par l'administrateur"
        self.save()

    def summary(self):
        if len(self.content) > 100 :
            return self.content[0:100] + "..."
        else :
            return self.content

    def requet_fixed(self):
        self.state = "Problème Résolu"
        self.fix_date = timezone.now()
        self.save()

    def requet_note(self):
        self.state = "notée"
        self.save()

    def repair_time(self):
        time = self.fix_date - self.pub_date
        hours = time.seconds // 3600
        minute = (time.seconds % 3600) // 60
        return str(time.days) + "days ," + str(hours) + "Hour ," + str(minute) + "minutes"


class Notification(models.Model):

    content = models.TextField()
    owner = models.ForeignKey(User , on_delete = models.CASCADE , related_name = "nots")
    requet = models.ForeignKey(Requet , on_delete = models.CASCADE , related_name = "nots")
