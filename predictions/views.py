from django.shortcuts import render, redirect, get_object_or_404
from .utils.scraper import get_economic_indicators 
from authuser.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate 
from django.db import IntegrityError
from .forms import ClientForm, UploadClientsForm
from django.contrib import messages
from .models import Client
import pandas as pd


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


def single_prediction(request):
    if request.method == 'GET':
        return render(request, 'single_prediction.html', {
        'form': ClientForm
    })

    else:
       
        form = ClientForm(request.POST)
        
        if form.is_valid():
            new_client = form.save(commit=False)
            new_client.user = request.user
            new_client.save()
           
            try:
                new_client.clean()

                if new_client.outcome_target == 'no':
                    message_to_user = f'The client {new_client} is not likely to take a term deposit.'
                    messages.error(request, message_to_user)
                else:
                    message_to_user = f'The client {new_client} is likely to take a term deposit.'
                    messages.success(request, message_to_user)

                return render(request, 'single_prediction.html', {
                    'form': form   
                })
            except ValueError as e:
                return render(request, 'single_prediction.html', {
                    'form': form,
                    'errors': e.message_dict    
                })
        
        else: 
            return render(request, 'single_prediction.html', {
                'form': form,
                'errors': form.errors
        })
 
        

        
def multiple_predictions(request):
    if request.method == 'GET':
        return render(request, 'multiple_predictions.html', {
            'form': UploadClientsForm
        })
    else:
        form = UploadClientsForm(request.POST, request.FILES)
        
        if form.is_valid():
            file = request.FILES['file']
            columns = pd.read_pickle('model/pickle_files/input_data_columns.pickle')
            total_columns = ['full_name'] + columns
            
            clients_data_from_file = pd.read_csv(file, sep=';', encoding='utf-8', names=total_columns)
            
            #print(clients_data_from_file.head())
            number_of_rows = clients_data_from_file.shape[0]

            for row in range(number_of_rows):

                new_client = Client.objects.create(
                    full_name = clients_data_from_file.loc[row, 'full_name'],
                    age = clients_data_from_file.loc[row, 'age'],
                    job = clients_data_from_file.loc[row, 'job'],
                    marital = clients_data_from_file.loc[row, 'marital'],
                    education = clients_data_from_file.loc[row, 'education'],
                    default = clients_data_from_file.loc[row, 'default'],
                    balance = clients_data_from_file.loc[row, 'balance'],
                    housing = clients_data_from_file.loc[row, 'housing'],
                    loan = clients_data_from_file.loc[row, 'loan'],
                    contact = clients_data_from_file.loc[row, 'contact'],
                    day = clients_data_from_file.loc[row, 'day'],
                    month = clients_data_from_file.loc[row, 'month'],
                    duration = clients_data_from_file.loc[row, 'duration'],
                    campaign = clients_data_from_file.loc[row, 'campaign'],
                    pdays = clients_data_from_file.loc[row, 'pdays'],
                    previous = clients_data_from_file.loc[row, 'previous'],
                    poutcome = clients_data_from_file.loc[row, 'poutcome'],
                    user = request.user
                )
                new_client.save()

                    
            
            return render(request, 'multiple_predictions.html', {
            'form': form
        })
        else:
            return render(request, 'multiple_predictions.html', {
            'form': UploadClientsForm,
            'errors': form.errors['file']
        })