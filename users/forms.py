from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm , UserChangeForm
from .models import Profile ,Personne ,Company ,Address
from django.utils.translation import gettext_lazy as _



class UserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ["username","email","password1","password2"]

        widgets = {
        "username" : forms.TextInput(attrs={ "class":"form-control username" ,"id":"username" ,"aria-describedby":"emailHelp" ,"placeholder":"Nom d'utilisateur"}),
        "email" : forms.TextInput(attrs={ "class":"form-control email" ,"id":"email" ,"aria-describedby":"emailHelp" ,"placeholder":"Votre Email Adress"}),
        }

        labels = {
            "username" : "",
            "email" : "",
        }

        help_texts = {
            "username" : None ,
            "password" : _("le mot de passe doit comporter plus de 8 caractères" ),
            "email" : None,
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
        self.fields['password1'].widget = forms.PasswordInput(attrs={"class":"form-control password" ,"id":"pass1" ,"placeholder":"mot de passe"})
        self.fields['password2'].widget = forms.PasswordInput(attrs={"class":"form-control password" ,"id":"pass2" ,"placeholder":"Retaper Le mot de passe"})
        self.fields['password1'].label = ""
        self.fields['password2'].label = ""
        self.fields['password1'].help_text = ""
        self.fields['password2'].help_text = ""


  # <-----------------------------                Profile Form        --------------------------->


class ProfileForm(forms.ModelForm):

    class Meta :

        model = Profile
        fields = ["phone_number"]
        widgets = {
                    "phone_number" : forms.TextInput(attrs={ "class":"form-control " ,"id":"phone" ,"aria-describedby":"emailHelp" ,"placeholder":"Votre telephone fix"}),
                    }

        labels = {
            "phone_number" : "",
        }

    def clean(self):
        data = super().clean()
        phone = data["phone_number"]
        if phone[0] != '0' :
            raise forms.ValidationError("entrer votre numéro fix !!")
        elif len(phone) != 9 :
            raise forms.ValidationError("entrer votre numéro fix seulement!!")
        else :
            return data

# <------------------------------- changing user information form ----------------------------->

#get all the existing emails


class UserChangeInfoForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ("email",)
        widgets = {
        "email" : forms.TextInput(attrs={ "class":"form-control email" ,"id":"exampleInputEmail1" ,"aria-describedby":"emailHelp" ,"placeholder":"Votre Email Adress"}),
        }


class ProfileChangeForm(forms.ModelForm):

    class Meta :
        model = Profile
        fields = ["phone_number"]
        widgets = {
                    "phone_number" : forms.TextInput(attrs={ "class":"form-control " ,"id":"exampleInputEmail1" ,"aria-describedby":"emailHelp" ,"placeholder":"Votre telephone fix"}),
        }

        labels = {
            "phone_number" : "Votre Telephone Fix",
        }

class PersonneChangeForm(forms.ModelForm):

    class Meta:
        model = Personne
        fields = ["first_name","last_name"]

        widgets = {
                    "first_name" : forms.TextInput(attrs={ "class":"form-control location" ,"id":"exampleInputEmail1" ,"aria-describedby":"emailHelp" ,"placeholder":"Nom"}),
                    "last_name" : forms.TextInput(attrs={ "class":"form-control " ,"id":"exampleInputEmail1" ,"aria-describedby":"emailHelp" ,"placeholder":"Prenon"}),
        }
        labels = {
            "first_name" : "Votre Nom",
            "last_name" : "Votre Prénom",
        }

class CompanyChangeForm(forms.ModelForm):

    class Meta:
        model = Company
        fields = ["name",]

        widgets = {
                    "name" : forms.TextInput(attrs={ "class":"form-control location" ,"id":"exampleInputEmail1" ,"aria-describedby":"emailHelp" ,"placeholder":"nom"}),
        }
        labels = {
            "name" : "Entrer le non de votre entreprise",
        }

class AddressCompanyChangeForm(forms.ModelForm):

    class Meta:

        REGIONS = [
        ("bouira" , "bouira"),
        ("hachimia" , "hachimia"),
        ("sour" , "sour"),
        ]

        model = Address
        fields = ["region","commune","rue"]

        widgets = {
        "region" : forms.Select(choices = REGIONS)
        }

        labels = {
            "region" : "Daira",
            "commune" : "la Commune",
            "rue" : "Rue",
        }

class AddressPersonneChangeForm(forms.ModelForm):

    class Meta:

        REGIONS = [
        ("bouira" , "bouira"),
        ("hachimia" , "hachimia"),
        ("sour" , "sour"),
        ]

        model = Address
        fields = ["region","commune","rue","logement"]

        widgets = {
        "region" : forms.Select(choices = REGIONS)
        }

        labels = {
            "region" : "Daira",
            "commune" : "la Commune",
            "rue" : "Rue",
            "logement" : "N° de Logement",
        }
