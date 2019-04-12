from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.utils.translation import gettext_lazy as _


class UserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ["username","first_name","last_name","email","password1","password2"]

        widgets = {
        "username" : forms.TextInput(attrs={ "class":"form-control username" ,"id":"exampleInputEmail1" ,"aria-describedby":"emailHelp" ,"placeholder":"Nom d'utilisateur"}),
        "first_name" : forms.TextInput(attrs={ "class":"form-control first-name" ,"id":"exampleInputEmail1" ,"aria-describedby":"emailHelp" ,"placeholder":"Votre Nom"}),
        "last_name" : forms.TextInput(attrs={ "class":"form-control last-name" ,"id":"exampleInputEmail1" ,"aria-describedby":"emailHelp" ,"placeholder":"Votre Prénom"}),
        "email" : forms.TextInput(attrs={ "class":"form-control email" ,"id":"exampleInputEmail1" ,"aria-describedby":"emailHelp" ,"placeholder":"Votre Email Adress"}),
        }

        labels = {
            "username" : "",
            "first_name" : "",
            "last_name" : "",
            "email" : "",
        }

        help_texts = {
            "username" : None ,
            "password" : _("le mot de passe doit comporter plus de 8 caractères" ),
            "email" : ("votre email doit être unique")
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
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={"class":"form-control password" ,"id":"exampleInputPassword1" ,"placeholder":"mot de passe"})
        self.fields['password2'].widget = forms.PasswordInput(attrs={"class":"form-control password" ,"id":"exampleInputPassword1" ,"placeholder":"Retaper Le mot de passe"})
        self.fields['password1'].label = ""
        self.fields['password2'].label = ""


  # <-----------------------------                Profile Form        --------------------------->


class ProfileForm(forms.ModelForm):

    class Meta :
        model = Profile
        fields = ["location"]
        widgets = {
                    "location" : forms.TextInput(attrs={ "class":"form-control location" ,"id":"exampleInputEmail1" ,"aria-describedby":"emailHelp" ,"placeholder":"Location"}),
        }
        labels = {
            "location" : ""
        }
