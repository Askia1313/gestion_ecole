from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.template.loader import render_to_string
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
import random
from django.views.decorators.csrf import csrf_protect
from .models import CustomUser
from .forms import UserRegistrationForm, CustomAuthenticationForm,UserUpdateForm
from .auth_backends import CustomBackend
from django.contrib.auth.decorators import login_required
from functools import wraps


def login_required_message(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.info(request, 'Veuillez vous connecter pour accéder aux cours.')
            return redirect('authentification:login_user')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def home(request):
    return render(request, "home.html")





def contact(request):
    return render(request, "contact.html")




def logout_user(request):
    logout(request)
    return redirect('authentification:home')


def login_user(request):
    message = ''
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = CustomBackend().authenticate(request, username=username, password=password)
            if user is not None:
                if not user.is_active:
                    message = 'Votre compte est inactif. Veuillez vérifier votre email pour activer votre compte.'
                    return render(request, 'activation.html', {'message': message})
                else:
                    user.backend = 'authentification.auth_backends.CustomBackend'  # Specify the backend
                    if user.est_prof is False:
                        auth_login(request, user)
                        return redirect('authentification:cours')
                    else:
                        auth_login(request, user)
                        return redirect('gestion_cours:gestion_cours')
            else:
                message = 'Identifiant ou mot de passe incorrect, veuillez réessayer.'
        else:
            message = 'Identifiant ou mot de passe incorrect, veuillez réessayer.'
    else:
        form = CustomAuthenticationForm()

    return render(request, 'login.html', {'form': form, 'message': message})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.num_mail = random.randint(100000, 999999)
            user.save()

            subject = "Activation de votre compte EDUCA"
            body = render_to_string('activate_email.html', {'user': user})

            send_mail(
                subject=subject,
                message=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
            send_mail.content_subtype = "html"

            return render(request, 'activation.html', {'user': user})
        else:
            messages.error(request, 'Le formulaire n\'est pas valide. Veuillez corriger les erreurs.')
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})

def forget_password(request):
    return render(request, "forget_password.html")

@csrf_protect
def verifier_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        code = request.POST.get('code')

        try:
            user = CustomUser.objects.get(email=email)
            if int(code) == int(user.num_mail):
                user.is_active = True
                user.save()
                user.backend = 'authentification.auth_backends.CustomBackend'  # Specify the backend
                auth_login(request, user)
                return redirect('authentification:cours')
            else:
                info2 = "Code invalide, veuillez réessayer"
                return render(request, "activation.html", {'info2': info2})
        except CustomUser.DoesNotExist:
            info2 = "Vous avez entré un mauvais email, veuillez réessayer"
            return render(request, "activation.html", {'info2': info2})
    else:
        return render(request, "activation.html")

def mes_infos(request):
    return render(request, "mes_infos.html")



from gestion_cours.models import Chapitre, Cours
from django.contrib.auth.decorators import login_required

@login_required_message
def cours(request):
    niveau = request.user.niveau
    matieres = Chapitre.objects.filter(niveau=niveau).values('matiere').distinct()
    chapitres = Chapitre.objects.filter(niveau=niveau)
    cours = Cours.objects.filter(chapitre__niveau=niveau)
    context = {
        'MEDIA_URL': settings.MEDIA_URL,
        'matieres': matieres,
        'chapitres': chapitres,
        'cours': list(cours.values('id', 'nom_cours', 'description', 'chapitre_id', 'cours_types', 'cours'))
    }
    return render(request, 'cours.html', context)





from django.core.mail import send_mail
from .forms import UserUpdateForm,CustomUser



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.template.loader import render_to_string
from django.conf import settings
import random

import random
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .forms import UserUpdateForm


@login_required
def update_profil(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            # Générer un code à 6 chiffres
            verification_code = random.randint(100000, 999999)

            # Sauvegarder le code de vérification
            request.session['verification_code'] = verification_code
            request.session['new_user_data'] = form.cleaned_data

            # Préparer et envoyer l'email de vérification
            subject = "Modification des informations"
            body = render_to_string('changement_info.html', {'user': request.user, 'code': verification_code})
            send_mail(
                subject=subject,
                message=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[request.user.email],
                fail_silently=False,
            )
            send_mail.content_subtype = "html"

            messages.success(request, 'Un email avec un code de vérification a été envoyé à votre adresse email.')

            return redirect('authentification:verify_code')  # Redirection vers la vue de vérification du code
        else:
            messages.error(request, 'Il y a eu une erreur dans le formulaire.')
    else:
        form = UserUpdateForm(instance=request.user)

    context = {
        'form': form
    }
    return render(request, 'mes_infos.html', context)


from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import views as auth_views

def password_reset_request(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('password_reset_done')
    else:
        form = PasswordResetForm()
    return render(request, 'password_reset_form.html', {'form': form})

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages



@login_required
def verify_code(request):
    if request.method == 'POST':
        entered_code = request.POST.get('verification_code')
        saved_code = request.session.get('verification_code')
        if str(saved_code) == entered_code:
            # Mettre à jour les informations utilisateur
            new_user_data = request.session.get('new_user_data')
            for field, value in new_user_data.items():
                setattr(request.user, field, value)
            request.user.num_mail = 0  # Réinitialiser le code de vérification
            request.user.save()

            # Nettoyer la session
            del request.session['verification_code']
            del request.session['new_user_data']

            messages.success(request, 'Vos informations ont été mises à jour avec succès.')
            return redirect('authentification:mes_infos')
        else:
            messages.error(request, 'Le code de vérification est incorrect.')

    return render(request, 'verify_code.html')


from django.shortcuts import render, get_object_or_404, redirect
from gestion_cours.models import Cours, Exercice, Question, Choice
from authentification.models import CustomUser


def exercice_list(request):
    user = request.user
    niveau = user.niveau  # Récupérer le niveau de l'utilisateur connecté
    exercices = Exercice.objects.filter(cours__chapitre__niveau=niveau)
    return render(request, 'exercice_list.html', {'exercices': exercices})

def quiz(request, exercice_id):
    exercice = get_object_or_404(Exercice, pk=exercice_id)
    questions = Question.objects.filter(exercice=exercice)
    results = request.session.pop('results', None)
    score = request.session.pop('score', None)
    return render(request, 'quiz.html', {
        'exercice': exercice,
        'questions': questions,
        'results': results,
        'score': score,
        'total': questions.count()
    })

def submit_quiz(request, exercice_id):
    if request.method == 'POST':
        score = 0
        results = []
        for question in Question.objects.filter(exercice_id=exercice_id):
            selected_choice_id = request.POST.get(str(question.id))
            if selected_choice_id:
                selected_choice = Choice.objects.get(id=selected_choice_id)
                correct_choice = Choice.objects.filter(question=question, is_correct=True).first()
                is_correct = selected_choice.is_correct
                if is_correct:
                    score += 1
                results.append({
                    'question_id': question.id,
                    'selected_choice_id': selected_choice.id,
                    'correct_choice_id': correct_choice.id,
                    'is_correct': is_correct
                })
        exercice = get_object_or_404(Exercice, pk=exercice_id)
        questions = Question.objects.filter(exercice=exercice)
        return render(request, 'quiz.html', {
            'exercice': exercice,
            'questions': questions,
            'results': results,
            'score': score,
            'total': questions.count()
        })
    return redirect('authentification:quiz', exercice_id=exercice_id)

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.core.mail import send_mail
from .forms import ProfCreationForm
import secrets
import string

def generate_random_password(length=8):
    characters = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password

def create_prof(request):
    password = generate_random_password()

    if request.method == 'POST':
        form = ProfCreationForm(request.POST)
        if form.is_valid():
            prof = form.save(commit=False)
            prof.set_password(form.cleaned_data['password1'])
            prof.save()
            send_welcome_email(prof, form.cleaned_data['password1'])
            return redirect('authentification:home')  # Redirect to home or another page on success
    else:
        form = ProfCreationForm(initial={'password1': password, 'password2': password})
        form.fields['password1'].widget.attrs['value'] = password
        form.fields['password2'].widget.attrs['value'] = password

    return render(request, 'create-prof.html', {'form': form, 'random_password': password})


def send_welcome_email(user, password):
    subject = 'Bienvenue en tant que Professeur'
    message = f'''
    Bonjour {user.prenom} {user.nom},

    Votre compte professeur a été créé avec succès. Voici vos informations de connexion :

    Email : {user.email}
    Numéro de téléphone : {user.telephone}
    Mot de passe : {password}


    Cordialement,
    L'équipe Educa
    '''
    from_email = 'konatefahran3@gmail.com'
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list)

