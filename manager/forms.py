from django import forms
from requets.models import Requet
from users.models import Profile ,Address
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _


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
        "tech" : "la possibilité de passer au technicien efficace"

        }

# <------------------------------- to add and admin or tech profile ------------------------------->

class AddAdminForm(UserCreationForm):

    class Meta:
        model = User
        fields = ["first_name","last_name","username","email","password1","password2"]

        widgets = {
        "username" : forms.TextInput(attrs={ "class":"form-control username" ,"id":"exampleInputEmail1" ,"aria-describedby":"emailHelp" ,"placeholder":"Nom d'utilisateur"}),
        "email" : forms.TextInput(attrs={ "class":"form-control email" ,"id":"exampleInputEmail1" ,"aria-describedby":"emailHelp" ,"placeholder":"Email Adress de l'employer"}),
        "first_name" : forms.TextInput(attrs={ "class":"form-control username" ,"id":"exampleInputEmail1" ,"aria-describedby":"emailHelp" ,"placeholder":"Nom"}),
        "last_name" : forms.TextInput(attrs={ "class":"form-control username" ,"id":"exampleInputEmail1" ,"aria-describedby":"emailHelp" ,"placeholder":"Prenom"}),
        }

        labels = {
            "username" : "",
            "email" : "",
            "first_name" : "",
            "last_name" : "",
        }

        help_texts = {
            "username" : None ,
            "password" : _("le mot de passe doit comporter plus de 8 caractères" ),
            "email" : ("email adress doit être unique")
        }


        # <---------------- changing the default error whene username already exists ------------------------->

    error_messages= {
        "username_exists": _("ce nom d'utilisateur existe déjà"),
        'password_mismatch': _("Les deux champs de mot de passe ne correspondent pas."),
        }



    def clean_username(self):
        username = self.cleaned_data.get("username")

        try:
            User._default_manager.get(username=username)
            #if the user exists, then let's raise an error message

            raise forms.ValidationError(
            self.error_messages['username_exists'],  #my error message

            code='username_exists',   #set the error message key

                )
        except User.DoesNotExist:
            return username # if user does not exist so we can continue the registration process



                    # <---------------- make the gmail a unique field  ------------------------->


    def clean_email(self):
        email1 = self.cleaned_data.get("email")
        username = self.cleaned_data.get("username")

        if User.objects.filter(email = email1).exclude(username = username).exists():
            raise forms.ValidationError(
            "l'adresse e-mail que vous avez entrée est déjà enregistrée, allez à la page de connexion et connectez-vous"
            )
        else :
            return email1


    def __init__(self, *args, **kwargs):
        super(AddAdminForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={"class":"form-control password" ,"id":"exampleInputPassword1" ,"placeholder":"mot de passe"})
        self.fields['password2'].widget = forms.PasswordInput(attrs={"class":"form-control password" ,"id":"exampleInputPassword1" ,"placeholder":"Retaper Le mot de passe"})
        self.fields['password1'].label = ""
        self.fields['password2'].label = ""

class ProfileAdminForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ["phone_number"]

        widgets = {
        "phone_number" : forms.TextInput(attrs={ "class":"form-control email" ,"id":"exampleInputEmail1" ,"aria-describedby":"emailHelp" }),
        }
        labels = {
                "phone_number" : "numéro telephone :",
        }

# <----------------------------- tech edit form ---------------------------------------------->
class UserChangeInfoForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ["email","first_name","last_name"]
        widgets = {
        "email" : forms.TextInput(attrs={ "class":"form-control email" ,"id":"exampleInputEmail1" ,"aria-describedby":"emailHelp" ,"placeholder":"Votre Email Adress"}),
        "first_name" : forms.TextInput(attrs={ "class":"form-control username" ,"id":"exampleInputEmail1" ,"aria-describedby":"emailHelp" ,"placeholder":"Nom"}),
        "last_name" : forms.TextInput(attrs={ "class":"form-control username" ,"id":"exampleInputEmail1" ,"aria-describedby":"emailHelp" ,"placeholder":"Prenom"}),
        }

        labels = {
                "email" : "Email adresse",
                "first_name" : "Nom",
                "last_name" : "Prenom",
        }

class AddressTechForm(forms.ModelForm):

    class Meta:
        REGIONS = [
        ("boira" , "bouira"),
        ("hachimia" , "hachimia"),
        ("sour" , "sour"),
        ]

        model = Address
        fields = ["region","commune","rue","logement"]

        widgets = {
        "region" : forms.Select(choices = REGIONS)
        }

        labels = {
            "region" : "Daira :",
            "commune" : "la Commune :",
            "rue" : "Rue :",
            "logement" : "N° de Logement :",
        }
