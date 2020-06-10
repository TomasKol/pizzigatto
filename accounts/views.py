from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from .forms import RegistrationForm, LogInForm

# Create your views here.
def basic(request):
  return render(request, 'accounts/accounts.html')

def signup_view(request):
  if request.method == 'POST':
    form = RegistrationForm(request.POST)
    if form.is_valid(): 
      user = form.save() 
      login(request, user)
      return redirect('menu:index')
  else:
    form = RegistrationForm()
  return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
  if request.method == 'POST':
    form = LogInForm(data=request.POST)
    if form.is_valid():
      user = form.get_user()
      login(request, user)
      if 'next' in request.POST:
        return redirect(request.POST.get('next'))
      return redirect('menu:index')
  else:
    form = LogInForm()
  return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
  logout(request)
  return redirect('menu:index')

