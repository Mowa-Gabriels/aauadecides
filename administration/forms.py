from votie.models import Position, Candidate
from django.forms import ModelForm
from django import forms

class PositionForm(ModelForm):

    class Meta:
        model = Position
        fields = ['text']
        widgets ={
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'col': 20})
        }

#class PollEditForm(ModelForm):



    #class Meta:
        #model = Poll
        #fields = ['text']
        #widgets ={
            #'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'col': 20})
        #}

class InfoForm(ModelForm):
        class Meta:
            model = Candidate
            fields = [
                'first_name',
                'last_name',
                'faculty',
                'description',
                'position',

            ]


class InfoEditForm(ModelForm):
    class Meta:
        model = Candidate
        fields = [
            'image',
            'first_name',
            'last_name',
            'faculty',
            'Department',
            'description',


        ]


def should_be_empty(value):
    if value:
        raise forms.ValidationError('Field not empty')

class Send_complaintForm(forms.Form):

    message = forms.CharField(widget=forms.Textarea)
    forcefield = forms.CharField(
        required=False, widget=forms.HiddenInput, label='leave empty', validators=[should_be_empty])


def empty(value):
    if value:
        raise forms.ValidationError('Field not empty')

class Send_updateForm(forms.Form):
    subject = forms.CharField(max_length=30)
    message = forms.CharField(widget=forms.Textarea)
    forcefield = forms.CharField(
        required=False, widget=forms.HiddenInput, label='leave empty', validators=[empty])

