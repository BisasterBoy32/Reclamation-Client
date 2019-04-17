from django.urls import path
from . import views
from django.contrib.auth.views import (
                                        PasswordResetView,
                                        PasswordResetConfirmView,
                                        PasswordResetDoneView,
                                        PasswordResetCompleteView,
)

urlpatterns = [
    path('',views.home,name="home"),
    path('create_requete/',views.RequetCreateView.as_view(),name="create_requete"),
    path('siuvi_requet/',views.RequetListView.as_view(),name="siuvi_requete"),
    path('delete_requet/<int:pk>/',views.RequetDeleteView.as_view(),name="delete_requete"),
    path('reset_password/',PasswordResetView.as_view(template_name="requets/reset_password.html"),name="reset_password"),
    path('password_reset_done/',PasswordResetDoneView.as_view(template_name="requets/reset_password_done.html"),name="password_reset_done"),
    path('password_reset_confirm/<uidb64>/<token>/',PasswordResetConfirmView.as_view(template_name="requets/reset_password_confirm.html"),name="password_reset_confirm"),
    path('password_reset_complete/',PasswordResetCompleteView.as_view(template_name="requets/reset_password_complete.html"),name="password_reset_complete"),
    path("tech_requets",views.TechRequetListView.as_view(),name="tech_requets")
]
