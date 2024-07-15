# authentification/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.CharField(unique=True, max_length=50)
    num_mail = models.IntegerField(default=0)
    telephone = models.CharField(max_length=15, blank=True, null=True ,unique=True)
    niveau = models.CharField(max_length=4, choices=[
        ('6e', '6eme'),
        ('5e', '5eme'),
        ('4e', '4eme'),
        ('3e', '3eme'),
        ('2nd', '2nd'),
        ('1ere', '1ere'),
        ('Tle', 'Tle'),
    ], blank=True, null=True)
    choix = models.IntegerField(default=0)
    ID_transaction=models.CharField( max_length=25, default=0)
    date_transaction=models.DateField(default='2000-01-01')
    nom = models.CharField(max_length=20, default="")
    prenom = models.CharField(max_length=20,default="")
    est_prof=models.BooleanField(default=False)
    prof_matricule= models.CharField(max_length=20, default="0000000")


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['telephone']

    def __str__(self):
        return self.email or self.telephone
