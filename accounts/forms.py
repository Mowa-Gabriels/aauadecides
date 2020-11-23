from django import forms
from votie.models import User, Voter
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

class VoterSignUpForm(UserCreationForm):
    matric_no = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control', 'type': 'email'}))
    password1 = forms.CharField(max_length=100,
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))

    class Meta:
        model = User
        fields = [
            'matric_no',
            'email',
            'password1',
            'password2',
        ]

    def __init__(self, *args, **kwargs):
        super(VoterSignUpForm, self).__init__(*args, **kwargs)

        self.fields['matric_no'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'


    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_active = True
        user.is_voter = True
        user.save()
        Voter.objects.create(user=user)
        return user

class AdminSignUpForm(UserCreationForm):
    matric_no = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control', 'type': 'email'}))
    password1 = forms.CharField(max_length=100,
                                    widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))

    class Meta:
        model = User
        fields = [
                'matric_no',
                'email',
                'password1',
                'password2'

            ]

    @transaction.atomic()
    def save(self):
        user = super().save(commit=False)
        user.is_active= True
        user.is_admin= True
        user.save()
        return user
