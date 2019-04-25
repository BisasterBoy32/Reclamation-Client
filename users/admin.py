from django.contrib import admin
from .models import Profile ,Personne ,Company , Address

# Register your models here.
admin.site.register(Profile)
admin.site.register(Personne)
admin.site.register(Company)
admin.site.register(Address)
