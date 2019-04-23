from django import forms
from .models import Requet

class RequetForm(forms.ModelForm):

    class Meta:
        model = Requet
        fields = ["problem","content",]

        CHOICES = [
        ("Coupage telephonique", "Coupage telephonique"),
        ("Autre Problem" ,"Autre Problem"),
        ]

        widgets = {
        "content" : forms.Textarea(attrs={"class":"form-control txa-requet" ,"id":"exampleFormControlTextarea1", "rows":"3"}),
        "problem" : forms.Select(choices = CHOICES , attrs={"required" : True})
        }

        labels = {
        "content" : "s'il vous plaît essayez de préciser votre problème"
        }


class InternetRequetForm(forms.ModelForm):

    class Meta:
        model = Requet
        fields = ["problem","content",]

        CHOICES = [
        ("Problem internet", "Problem internet"),
        ("Autre Problem" ,"Autre Problem"),
        ]

        widgets = {
        "content" : forms.Textarea(attrs={"class":"form-control txa-requet" ,"id":"exampleFormControlTextarea1", "rows":"3"}),
        "problem" : forms.Select(choices = CHOICES , attrs={"required" : True})
        }

        labels = {
        "content" : "s'il vous plaît essayez de préciser votre problème"
        }
