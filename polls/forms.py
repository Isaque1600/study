from django import forms
from .models import Choice, Questions


class QuestionsForm(forms.ModelForm):
    class Meta:
        model = Questions
        fields = ["question_text"]


class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ["choice_text"]
