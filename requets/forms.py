from django import forms
from .models import Requet

class RequetForm(forms.ModelForm):

    class Meta:
        model = Requet
        fields = ["content"]

        widgets = {
        "content" : forms.Textarea(attrs={"class":"form-control txa-requet" ,"id":"exampleFormControlTextarea1", "rows":"3"})
        }
        labels = {
        "content" : "s'il vous plaît essayez de préciser votre problème"
        }
