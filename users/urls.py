from django.urls import path , include
from . import views
from django.contrib.auth.views import (
                                        PasswordResetView,
                                        PasswordResetConfirmView,
                                        PasswordResetDoneView,
                                        PasswordResetCompleteView,
)


urlpatterns = [
    path('',views.register,name="register" ),
    path('login/',views.login_view,name="login" ),
    path('client_info/',views.user_info,name="client_info"),
    path('entreprise_info/',views.entreprise_info,name="entreprise_info"),
    path('logout/',views.logout_view,name="logout" ),
    path('reset_password/',PasswordResetView.as_view(template_name="requets/reset_password.html"),name="reset_password"),
    path('password_reset_done/',PasswordResetDoneView.as_view(template_name="requets/reset_password_done.html"),name="password_reset_done"),
    path('password_reset_confirm/<uidb64>/<token>/',PasswordResetConfirmView.as_view(template_name="requets/reset_password_confirm.html"),name="password_reset_confirm"),
    path('password_reset_complete/',PasswordResetCompleteView.as_view(template_name="requets/reset_password_complete.html"),name="password_reset_complete"),
    path('login_tech/',views.login_tech,name="login_tech" ),
    path('client/<int:id_client>/<int:id_requet>/',views.requet_info,name="requet_info" ),
    path("problem_fixed/<int:id>/",views.problem_fixed,name="problem_fixed"),
    path("note/<int:id_u>/<int:id_r>/",views.note_view,name="note"),
    path("success_register/",views.success_register,name="success_register"),
    path('confirm_user/<slug:uidb64>/<slug:token>)/', views.confirm_user, name='confirm_user'),
]
