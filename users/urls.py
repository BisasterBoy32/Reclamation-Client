from django.urls import path , include
from . import views

urlpatterns = [
    path('',views.register,name="register" ),
    path('login/',views.login_view,name="login" ),
]
