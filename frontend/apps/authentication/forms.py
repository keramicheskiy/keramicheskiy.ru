from django import forms
from django.core.validators import RegexValidator


class RegistrationForm(forms.Form):
    ORIENTATIONS = (
        (1, "Straight"),
        (2, "Gay"),
        (3, "Lesbian"),
        (4, "Bisexual"),
        (5, "Other"),
    )
    username = forms.CharField(min_length=1, max_length=50,
                               widget=forms.TextInput(attrs={'class': 'form-control'}),
                               validators=[RegexValidator(
                                   '[A-Za-z0-9_.-]*',
                                   message="Username should be a combination of letters, numbers, underscores, scores and dots", )])
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                             validators=[RegexValidator(
                                 '[A-Za-z0-9_.+-]*@[A-Za-z0-9-]*\.[A-Za-z0-9-]+',
                                 message="This is not email address", )])
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    sexual_orientation = forms.ChoiceField(
        choices=ORIENTATIONS, label='Выберите пол', widget=forms.Select(attrs={'class': 'form-control'})
    )


class LoginForm(forms.Form):
    username = forms.CharField(min_length=1, max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
