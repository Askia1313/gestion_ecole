from django.contrib import admin
from django.urls import path
from .views import home, contact, cours, login_user, register, forget_password, verifier_email, logout_user, mes_infos, verify_code, update_profil,exercice_list,quiz,submit_quiz,create_prof,password_reset_request
from django.contrib.auth import views as auth_views
app_name = 'authentification'

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('cours/', cours, name='cours'),
    path('', home, name='home'),
    path('contact/', contact, name='contact'),
    path('login_user/', login_user, name='login_user'),
    path('logout_user/', logout_user, name='logout_user'),
    path('register/', register, name='register'),
    path('forget_password/', forget_password, name='forget_password'),
    path('verifier_email/', verifier_email, name='verifier_email'),
    path('mes_infos/', mes_infos, name='mes_infos'),
    path('update_profil/', update_profil, name='update_profil'),
    path('verify_code/', verify_code, name='verify_code'),
    path('exercice_list/', exercice_list, name='exercice_list'),
    path('quiz/<int:exercice_id>/', quiz, name='quiz'),
    path('exercice/<int:exercice_id>/submit/', submit_quiz, name='submit_quiz'),
    path('create_prof/', create_prof, name='create_prof'),

    path('password_reset/', password_reset_request, name='password_reset_request'),
    path('reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
         name='password_reset_complete'),
]
