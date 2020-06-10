from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class LogInForm(AuthenticationForm):
  username = forms.CharField(
    widget=forms.TextInput(
      attrs={
        'placeholder': 'username', 
        'title': 'username', 
        'autofocus': 'true', 
        'autocomplete': 'off'
      }
    )
  )
  password = forms.CharField(widget=forms.PasswordInput(
      attrs={'placeholder': 'password', 'title': 'password'}))

  class Meta:
    model = User
    fields = ['username', 'password']


class RegistrationForm(UserCreationForm):
  
  username = forms.CharField(widget=forms.TextInput(
      attrs={'placeholder': 'username', 'title': 'username'}))
  first_name = forms.CharField(widget=forms.TextInput(
      attrs={'placeholder': 'first name', 'title': 'first name'}))
  last_name = forms.CharField(widget=forms.TextInput(
      attrs={'placeholder': 'last name', 'title': 'last name'}))
  email = forms.EmailField(widget=forms.EmailInput(
      attrs={'placeholder': 'email', 'title': 'email'}))
  password1 = forms.CharField(widget=forms.PasswordInput(
      attrs={'placeholder': 'password', 'title': 'password'}))
  password2 = forms.CharField(widget=forms.PasswordInput(
      attrs={'placeholder': 'confirm password', 'title': 'confirm password'}))


  class Meta:
    model = User
    fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2',]

  def save(self, commit=True):
    user = super(RegistrationForm, self).save(commit=False)
    user.first_name = self.cleaned_data['first_name']
    user.last_name = self.cleaned_data['last_name']
    user.email = self.cleaned_data['email']

    if commit:
      user.save()

    return user
