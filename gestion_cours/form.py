from django import forms
from .models import Chapitre, Cours


class ChapitreForm(forms.ModelForm):
    class Meta:
        model = Chapitre
        fields = ['niveau', 'matiere', 'nom']


class CoursForm(forms.ModelForm):
    class Meta:
        model = Cours
        fields = ['nom_cours', 'description', 'chapitre', 'cours', 'cours_types']


class ChapitreCoursForm(forms.ModelForm):
    chapitre = forms.ModelChoiceField(queryset=Chapitre.objects.all(), empty_label="Sélectionner un chapitre existant",
                                      required=False)
    nouveau_chapitre = ChapitreForm()

    class Meta:
        model = Cours
        fields = ['nom_cours', 'description', 'chapitre', 'cours', 'cours_types']



from django import forms
from .models import Exercice, Question, Choice

class ExerciceForm(forms.ModelForm):
    class Meta:
        model = Exercice
        fields = ['titre', 'cours']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['exercice', 'question_text']

ChoiceFormSet = forms.modelformset_factory(
    Choice,
    fields=('choice_text', 'is_correct'),
    extra=3,
)
