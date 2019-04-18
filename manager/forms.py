from django import forms
from requets.models import Requet
from django.contrib.auth.models import User


class  EditRequetForm(forms.ModelForm):

    def __init__(self,*args,**kwargs):
        super (EditRequetForm,self ).__init__(*args,**kwargs) # populates the post
        self.fields['tech'].queryset = User.objects.filter(profile__group = "tech")

    class Meta:
        model = Requet
        fields = ["content" , "tech"]

        widgets = {
        "content" : forms.Textarea(attrs={"class" : "form-control" ,"id" : "exampleFormControlTextarea1" , "rows" : "3"})
        }
        
        labels = {
        "content" : "modifier le contenu pour être plus clair",
        "tech" : "la capacité de passer au technicien efficace"

        }
