from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from users.models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class ProfileForm(forms.ModelForm):
    genderChoices = (
        ('man', 'Man'),
        ('woman', 'Woman'),
    )
    gender = forms.CharField(widget=forms.Select(choices=genderChoices))
    birth_date = forms.DateTimeField(widget=forms.DateTimeInput(format='%d/%m/%Y', attrs={'type': 'datetime'}))
    countryChoices = (
        ('kz', 'Kazakhstan'),
        ('usa', 'USA'),
    )
    country = forms.CharField(widget=forms.Select(choices=countryChoices))
    cityChoices = (
        ('astana', 'Astana'),
        ('almaty', 'Almaty'),
        ('los_angeles', 'Los Angeles'),
        ('texas', 'Texas'),
    )
    city = forms.CharField(widget=forms.Select(choices=cityChoices))
    higher_educationChoices = (
        ('yes', 'Yes'),
        ('no', 'No'),
    )
    higher_education = forms.CharField(widget=forms.Select(choices=higher_educationChoices))

    class Meta:
        model = Profile
        fields = ['gender', 'birth_date', 'country', 'city', 'higher_education']
