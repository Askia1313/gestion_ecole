from django.db import models
from authentification.models import CustomUser
class Chapitre(models.Model):

    niveau = models.CharField(max_length=4, choices=[
        ('6e', '6eme'),
        ('5e', '5eme'),
        ('4e', '4eme'),
        ('3e', '3eme'),
        ('2nd', '2nd'),
        ('1ere', '1ere'),
        ('Tle', 'Tle'),
    ], blank=True, null=True)
    matiere = models.CharField(max_length=20, choices=[
        ('MATHEMATIQUE','MATHEMATIQUE'),
        ('PHYSIQUE-CHIMIE','PHYSIQUE-CHIMIE'),
        ('HISTOIRE-GEOGRAPHIE','HISTOIRE-GEOGRAPHIE'),
        ('ANGLAIS','ANGLAIS'),
        ('PHILOSOPHIE','PHILOSOPHIE'),
        ('ALLEMAND','ALLEMAND'),
        ('SVT','SVT'),
    ], blank=True, null=True)
    nom= models.CharField(max_length=100, default='')
    def __str__(self):
        return self.nom

class Cours(models.Model):
    nom_cours = models.CharField(max_length=200,default='')
    description = models.TextField(default='')
    chapitre = models.ForeignKey(Chapitre, on_delete=models.CASCADE,default=1)
    cours = models.FileField(upload_to='media/', default='')
    creator_email = models.EmailField(default='')
    cours_types = models.CharField(max_length=5, choices=[
        ('.pdf', 'texte'),
        ('.mp4', 'video'),
        ('.jpeg','image'),

    ], blank=True, null=True)
    def __str__(self):
        return self.nom_cours


class Exercice(models.Model):
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE,default=1)
    titre = models.CharField(max_length=255,default='')
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE,default=1)
    def __str__(self):
        return self.titre

class Question(models.Model):
    exercice = models.ForeignKey(Exercice, on_delete=models.CASCADE,default=1)
    question_text = models.CharField(max_length=255)

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text