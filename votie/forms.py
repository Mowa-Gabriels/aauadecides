from .models import Poll, Choice
from django.forms import ModelForm
from django import forms

class PollForm(ModelForm):
    choice1 = forms.CharField(
        label='First Choice',
        max_length=100,
        min_length=3,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Poll
        fields = ['text']
        widgets ={
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'col': 20})
        }

class PollEditForm(ModelForm):



    class Meta:
        model = Poll
        fields = ['text']
        widgets ={
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'col': 20})
        }

class ChoiceForm(ModelForm):
        class Meta:
            model = Choice
            fields = ['choice_text']

class ChoiceEditForm(ModelForm):
        class Meta:
            model = Choice
            fields = ['choice_text', 'choice_image']