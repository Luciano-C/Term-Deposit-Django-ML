from django.shortcuts import render, redirect, get_object_or_404
from .utils.scraper import get_economic_indicators 
from authuser.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate 
from django.db import IntegrityError


# Create your views here.
def home(request):
    economic_indicators = get_economic_indicators()
    return render(request, 'home.html', {
        'dollar_bid': economic_indicators['dollar']['bid'],
        'dollar_ask': economic_indicators['dollar']['ask'],
        'euro_bid': economic_indicators['euro']['bid'],
        'euro_ask': economic_indicators['euro']['ask']
    })

def read_more(request):
    return render(request, 'read_more.html')


def signin(request):
    if request.method == "GET":
        return render(request, 'signin.html')
    else:
        user = authenticate(
            request, email=request.POST['email'], password=request.POST['password']
        ) 
        
        if user is None:
            return render(request, 'signin.html', {
                'error': 'Email or password incorrect'
            })
        else:
            login(request, user)
            return redirect('predictions') 

def signup(request):
    if request.method == "GET":
        return render(request, 'signup.html')
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(email=request.POST['email'])
                user.set_password(request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('predictions')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'error': 'Email already exists'
                })
            
@login_required            
def signout(request):
    logout(request)
    return redirect('home')


def predictions(request):
    return render(request, 'predictions.html')