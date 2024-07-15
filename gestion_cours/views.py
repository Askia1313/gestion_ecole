# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cours
from .form import CoursForm, ChapitreForm

from django.conf import settings

@login_required
def gestion_cours(request):
    user_courses = Cours.objects.filter(creator_email=request.user.email)
    context = {
        'user_courses': user_courses,
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request, 'gestion_cours.html', context)



@login_required
def ajout_cours(request):
    form_cours = CoursForm()
    form_chapitre = ChapitreForm()

    if request.method == 'POST':
        if 'ajouter_cours' in request.POST:
            form_cours = CoursForm(request.POST, request.FILES)
            if form_cours.is_valid():
                cours = form_cours.save(commit=False)
                cours.creator_email = request.user.email
                cours.save()
                return redirect('gestion_cours:gestion_cours')

        elif 'ajouter_chapitre' in request.POST:
            form_chapitre = ChapitreForm(request.POST)
            if form_chapitre.is_valid():
                form_chapitre.save()
                return redirect('gestion_cours:ajout_cours')

    context = {
        'form_cours': form_cours,
        'form_chapitre': form_chapitre,
    }
    return render(request, 'ajout_cours.html', context)

@login_required
def supprimer_cours(request, course_id):
    course = get_object_or_404(Cours, id=course_id, creator_email=request.user.email)
    course.delete()
    return redirect('gestion_cours:gestion_cours')


from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Question, Choice


def quiz(request):
    questions = Question.objects.all()
    results = request.session.pop('results', None)
    score = request.session.pop('score', None)
    total = Question.objects.count()

    if results:
        for result in results:
            result['question'] = Question.objects.get(id=result['question_id'])
            result['selected_choice'] = Choice.objects.get(id=result['selected_choice_id'])
            result['correct_choice'] = Choice.objects.get(id=result['correct_choice_id'])

    return render(request, 'quiz.html', {
        'questions': questions,
        'results': results,
        'score': score,
        'total': total,
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
        request.session['results'] = results
        request.session['score'] = score
        return redirect('quiz_results')
    return redirect('quiz', exercice_id=exercice_id)







from django.shortcuts import render, redirect, get_object_or_404
from .models import Exercice, Question, Choice, Cours

from django.shortcuts import render, redirect
from .models import Cours, Exercice, Question, Choice


from django.shortcuts import render, redirect
from .models import Exercice, Question, Choice
from .form import ExerciceForm, QuestionForm, ChoiceFormSet

def ajout_exercice (request):
    exercice_form = ExerciceForm(request.POST or None)
    question_form = QuestionForm(request.POST or None)
    choice_formset = ChoiceFormSet(request.POST or None, queryset=Choice.objects.none())

    if request.method == 'POST':
        exercice_form = ExerciceForm(request.POST)
        if exercice_form.is_valid():
            exercice = exercice_form.save(commit=False)
            exercice.creator = request.user
            exercice.save()
            return redirect('gestion_cours:ajout_exercice')

        elif 'save_question' in request.POST:
            if question_form.is_valid() and choice_formset.is_valid():
                question = question_form.save()
                choices = choice_formset.save(commit=False)
                for choice in choices:
                    choice.question = question
                    choice.save()
                return redirect('gestion_cours:ajout_exercice')

    context = {
        'exercice_form': exercice_form,
        'question_form': question_form,
        'choice_formset': choice_formset,
    }
    return render(request, 'ajout_exercice.html', context)


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Question, Choice,Exercice,Cours

@login_required
def mes_questions(request):
    # Récupérer tous les exercices de l'utilisateur connecté
    exercises = Exercice.objects.filter(creator=request.user)

    context = {
        'exercises': exercises,
    }
    return render(request, 'mes_questions.html', context)
@login_required
def supprimer_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    # Supprimer les choix associés à la question
    choices = Choice.objects.filter(question=question)
    choices.delete()

    # Supprimer la question elle-même
    question.delete()

    return redirect('gestion_cours:mes_questions')
