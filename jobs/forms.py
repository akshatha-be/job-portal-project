from django import forms
from .models import Job,Application
from django.contrib.auth.models import User

class JobForm(forms.ModelForm):

    class Meta:
        model = Job
        fields = ['title','company','location','salary','description']


class ApplicationForm(forms.ModelForm):

    class Meta:
        model = Application
        fields = ['resume','cover_letter']


class RegisterForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username','email','password']