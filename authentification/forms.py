from django.contrib.auth.forms import AuthenticationForm

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'telephone', 'nom', 'prenom', 'niveau')

    def save(self, commit=True):
        user = super().save(commit=False)
        if not user.username:  # Assurez-vous de ne pas écraser un nom d'utilisateur existant
            user.username = user.email or user.telephone  # Utilisez l'email ou le téléphone comme nom d'utilisateur unique
        if commit:
            user.save()
        return user


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Email or Phone', max_length=254)

    def confirm_login_allowed(self, user):
        # Ne rien faire ici pour éviter les vérifications d'état actif/inactif
        pass




class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'telephone', 'niveau',   'nom', 'prenom']

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)



from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
import secrets
import string

class ProfCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'telephone', 'nom', 'prenom', 'prof_matricule')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.est_prof = True
        user.is_active = True
        if not user.username:  # Assurez-vous de ne pas écraser un nom d'utilisateur existant
            user.username = user.email or user.telephone  # Utilisez l'email ou le téléphone comme nom d'utilisateur unique
        if commit:
            user.save()
        return user

