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
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings

User = get_user_model()

def password_reset_request(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data['email']
            try:
                user = User.objects.get(email=data)
            except User.DoesNotExist:
                info= "cet utilisateurs n'existe pas."
                return render(request, 'password_reset_form.html', {'form': form, 'info': info})

            subject = "modification de votre mot de passe"
            email_template_name = "password_reset_email.html"
            context = {
                "email": user.email,
                'domain': request.META['HTTP_HOST'],
                'site_name': 'educa',
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "user": user,
                'token': default_token_generator.make_token(user),
                'protocol': 'http',
            }
            email = render_to_string(email_template_name, context)
            send_mail(subject, email, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
            return redirect('authentification:password_reset_done')
    else:
        form = PasswordResetForm()
    return render(request, 'password_reset_form.html', {'form': form})


def password_reset_complete(request):
    return redirect('authentification:login')
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



from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import datetime
from random import randint
from django.conf import settings
from .models import CustomUser
import requests

API_KEY = "MAGPMLT3QFJLIPUDN"
BEARER_TOKEN = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZF9hcHAiOjE1MDA5LCJpZF9hYm9ubmUiOjg5OTQyLCJkYXRlY3JlYXRpb25fYXBwIjoiMjAyNC0wNC0wOCAwODozMjoyNCJ9.NRcyHfFO8OyaXOaklZ2DJ2Arf-gV8OXGfMIELQzdw88"

def payin_with_redirection(transaction_id, nom, prenom, email, total_price):
    url = "https://app.ligdicash.com/pay/v01/redirect/checkout-invoice/create"
    payload = {
        "commande": {
            "invoice": {
                "items": [
                    {
                        "name": "Abonnement EDUCA",
                        "description": "Abonnement aux cours sur EDUCA",
                        "quantity": 1,
                        "unit_price": total_price,
                        "total_price": total_price
                    }
                ],
                "total_amount": total_price,
                "devise": "XOF",
                "description": "Abonnement aux cours sur EDUCA",
                "customer": "",
                "customer_firstname": nom,
                "customer_lastname": prenom,
                "customer_email": email
            },
            "store": {
                "name": "EDUCA",
                "website_url": "http://localhost/APP1/"
            },
            "actions": {
                "cancel_url": "http://127.0.0.1:8000/APP1/",
                "return_url": "http://127.0.0.1:8000/APP1/cours",
                "callback_url": "http://127.0.0.1:8000/APP1/ligdicash-callback/"  # Callback URL configurée
            },
            "custom_data": {
                "transaction_id": transaction_id
            }
        }
    }
    headers = {
        "Apikey": API_KEY,
        "Authorization": BEARER_TOKEN,
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.ok:
        return response.json()
    else:
        return {"response_code": response.status_code, "response_text": "Erreur lors de la requête HTTP"}

def paiement(request):
    if request.method == 'POST':
        # Récupérer les données du formulaire
        type_abonnement = request.POST.get('type_abonnement')
        total_price = 100 if type_abonnement == 'standard' else 150
        choix = 1 if type_abonnement == 'standard' else 2

        # Récupérer les informations de l'utilisateur
        user = request.user
        nom = user.last_name
        prenom = user.first_name
        email = user.email

        transaction_id = f"EDUCA{datetime.now().strftime('%Y%m%d_%H%M')}.C{randint(5, 100000)}"

        # Appel à l'API Ligdicash pour créer une commande
        redirect_payin = payin_with_redirection(transaction_id, nom, prenom, email, total_price)

        # Vérifiez et traitez la réponse
        if 'response_code' in redirect_payin:
            response_code = redirect_payin['response_code']
            if response_code == "00":
                # Stocker les informations dans la session
                request.session['choix'] = choix
                request.session['transaction_id'] = transaction_id
                user.ID_transaction = transaction_id
                user.save()

                # Redirection vers l'URL de paiement
                return redirect(redirect_payin['response_text'])
            else:
                # Gestion des erreurs
                response_text = redirect_payin.get('response_text', '')
                description = redirect_payin.get('description', '')
                return HttpResponse(f"Erreur {response_code}: {response_text}<br><br>{description}")
        else:
            return HttpResponse("Une erreur s'est produite lors de la demande de paiement.")
    else:
        # Afficher le formulaire HTML
        return render(request, 'abonnement.html')



from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

@csrf_exempt
def verifier_transaction(request, transaction_id):
    url = f"https://app.ligdicash.com/pay/v01/redirect/checkout-invoice/confirm/?invoiceToken={transaction_id}"
    headers = {
        'Apikey': API_KEY,
        'Authorization': BEARER_TOKEN,
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers)

    if response.ok:
        response_data = response.json()
        status = response_data.get('status')
        if status == 'completed':
            # Mettre à jour l'utilisateur
            user = request.user
            user.choix = request.session.get('choix', user.choix)
            user.save()
            return redirect('cours')  # Redirection vers la page de cours
        else:
            return HttpResponse("La transaction n'a pas été complétée.")
    else:
        return HttpResponse("Erreur lors de la vérification de la transaction.")
