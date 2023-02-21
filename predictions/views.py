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
from datetime import datetime
import numpy as np


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
            'form': UploadClientsForm,
        })
    else:
        form = UploadClientsForm(request.POST, request.FILES)
        try:
            if form.is_valid():
                # Gets file
                file = request.FILES['file']
                # Creates a variable for the columns of the dataframe
                columns = pd.read_pickle('model/pickle_files/input_data_columns.pickle')
                total_columns = ['full_name'] + columns
                
                # Load data from file into dataframe with the column names
                clients_data_from_file = pd.read_csv(file, sep=';', encoding='utf-8', names=total_columns)
                
                #print(clients_data_from_file.head())
                
                # number_of_rows and predictions for itetarion
                number_of_rows = clients_data_from_file.shape[0]
                predictions = []

                for row in range(number_of_rows):
                    # Creates a record in database for each row in the dataframe
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
                    # Adds the prediction result, which will be used for the chart
                    predictions.append(new_client.outcome_target)
                
                # Adds a column with the predictions to the dataframe
                clients_data_from_file['predictions'] = predictions
                # Prepares the data for the chart as a list with ['yes', 'no'] values
                data_for_chart = [clients_data_from_file['predictions'].value_counts()['yes'], clients_data_from_file['predictions'].value_counts()['no']]
                
                return render(request, 'multiple_predictions.html', {
                'form': form,
                'data': data_for_chart
            })

            else:
                return render(request, 'multiple_predictions.html', {
                'form': UploadClientsForm,
                'errors': form.errors['file']
            })
        except:
            form.add_error('file', 'There is a problem with the file.')
            return render(request, 'multiple_predictions.html', {
                'form': UploadClientsForm,
                'errors': form.errors['file']
            })
        


def my_predictions(request):
    user_clients = Client.objects.filter(user=request.user)
    return render(request, 'my_predictions.html', {
        'user_clients': user_clients
    })


def manage_client(request, client_id):
    if request.method == 'GET':
        client = get_object_or_404(Client, pk=client_id, user=request.user)
        form = ClientForm(instance=client)

        return render(request, 'manage_client.html', {
            'client': client,
            'form': form
        })
    
    elif request.method == 'POST':
        if request.POST.get('_method') == 'PUT':
            try:
                client = get_object_or_404(Client, pk=client_id, user=request.user)
                form = ClientForm(request.POST.copy(), instance=client)
                form.save()
                return redirect('my_predictions')
            except ValueError:
                form = ClientForm(request.POST.copy(), instance=client)
                return render(request, 'manage_client.html', {
                    'form': form,
                    'errors': form.errors
                })
        else:
            # Handle other POST requests here
            client = get_object_or_404(Client, pk=client_id, user=request.user)
            client.delete()
            return redirect('my_predictions')


def search_clients(request):
    clients = Client.objects.filter(user=request.user)
    print(request.GET)
    print(request.GET['name-search'])
    
    if request.method == 'GET':
    
        if request.GET['name-search']:
            name_search = request.GET['name-search']
            clients = clients.filter(full_name__icontains=name_search)
        if request.GET['outcome-search']:
            outcome_search = request.GET['outcome-search']
            clients = clients.filter(outcome_target__icontains=outcome_search)
        if request.GET['date-search']:
            date_search = request.GET['date-search']
            formatted_date = datetime.strptime(date_search, '%Y-%m-%d')
            start_date = formatted_date
            end_date = formatted_date.replace(hour=23, minute=59, second=59)
            clients = clients.filter(updated_at__range=[start_date, end_date])

            
            #formatted_date = datetime.strptime(date_search, '%Y-%m-%d').strftime('%d-%m-%Y')
              
            
        return render(request,'my_predictions.html', {
        'user_clients': clients,
        'name_search_value': request.GET['name-search'],
        'outcome_search_value': request.GET['outcome-search']
    })


def charts(request):
    # Age Chart
    age_bins = np.arange(0, 110, 10)
    age_labels = np.arange(10, 110, 10)
    
    yes_clients = Client.objects.filter(user=request.user, outcome_target='yes')
    yes_ages = [client.age for client in yes_clients]
    yes_df = pd.DataFrame(yes_ages, columns=['age'])
    yes_df['label'] = pd.cut(x = yes_df['age'], bins=age_bins, labels=age_labels, include_lowest=True)
    yes_count = yes_df['label'].value_counts().sort_index()


    no_clients = Client.objects.filter(user=request.user, outcome_target='no')
    no_ages = [client.age for client in no_clients]
    no_df = pd.DataFrame(no_ages, columns=['age'])
    no_df['label'] = pd.cut(x = no_df['age'], bins=age_bins, labels=age_labels, include_lowest=True)
    no_count = no_df['label'].value_counts().sort_index()
    
    

    
    

    
    
    return render(request, 'charts.html',{
        'age_labels': list(age_labels),
        'age_yes_count': list(yes_count.values),
        'age_no_count': list(no_count.values)
    })
  
   