from django.contrib import admin
from django.urls import path
from .views import gestion_cours, ajout_cours,supprimer_cours,quiz,submit_quiz,ajout_exercice,mes_questions,supprimer_question
app_name = 'gestion_cours'

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('gestion_cours/', gestion_cours, name='gestion_cours'),
    path('ajout_cours/', ajout_cours, name='ajout_cours'),
    path('supprimer_cours/<int:course_id>/', supprimer_cours, name='supprimer_cours'),
    path('quiz/', quiz, name='quiz'),
    path('submit_quiz/', submit_quiz, name='submit_quiz'),
    path('ajout_exercice/', ajout_exercice, name='ajout_exercice'),
    path('mes_questions/', mes_questions, name='mes_questions'),
    path('supprimer_exercice/<int:question_id>/', supprimer_question, name='supprimer_question'),
]


