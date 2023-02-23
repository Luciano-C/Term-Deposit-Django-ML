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
from .utils.chart_data import get_numeric_chart_data, get_categorical_chart_data
import json


# Create your views here.
def home(request):
    # Calls the webscraper
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

@login_required
def predictions(request):
    return render(request, 'predictions.html')

@login_required
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
                # Checks if there are any errors in the input
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
 
        

@login_required       
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
                'number_of_yes_clients': [clients_data_from_file['predictions'].value_counts()['yes']],
                'number_of_no_clients':[clients_data_from_file['predictions'].value_counts()['no']]
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
        

@login_required
def my_predictions(request):
    user_clients = Client.objects.filter(user=request.user)
    return render(request, 'my_predictions.html', {
        'user_clients': user_clients
    })

@login_required
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
            client = get_object_or_404(Client, pk=client_id, user=request.user)
            client.delete()
            return redirect('my_predictions')

@login_required
def search_clients(request):
    clients = Client.objects.filter(user=request.user)
    
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
            # Creates a start and end date with the same date but at 23:59:59. This is done because the date in the database is a datetimefield and this accounts for the time.
            start_date = formatted_date
            end_date = formatted_date.replace(hour=23, minute=59, second=59)
            clients = clients.filter(updated_at__range=[start_date, end_date])
    
        return render(request,'my_predictions.html', {
        'user_clients': clients,
        'name_search_value': request.GET['name-search'],
        'outcome_search_value': request.GET['outcome-search']
    })

@login_required
def charts(request):
    total_clients = Client.objects.filter(user=request.user)
    
    # Months are ordered accordingly before being sent to the charts
    month_order = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
    if len(total_clients) > 2:
        months_labels = get_categorical_chart_data(total_clients, 'month')['labels']
        ordered_month_labels = sorted(months_labels, key=lambda x: month_order.index(x))
    else:
        ordered_month_labels = month_order

    # Something JSON.parse on the template wasn't working with the list os strings, so the list is serialized as a JSON formatted string
    # with json.dumps
    
   
    return render(request, 'charts.html',{
        # intro
        'number_of_clients': total_clients.count(),
        'number_of_yes_clients': [total_clients.filter(outcome_target='yes').count()],
        'number_of_no_clients': [total_clients.filter(outcome_target='no').count()],
        # age
        'age_labels': get_numeric_chart_data(total_clients, 'age')['labels'],
        'age_yes_count': get_numeric_chart_data(total_clients, 'age')['attribute_yes_count'],
        'age_no_count': get_numeric_chart_data(total_clients, 'age')['attribute_no_count'],
        # job
        'job_labels': json.dumps(get_categorical_chart_data(total_clients, 'job')['labels']),
        'job_yes_count':  get_categorical_chart_data(total_clients, 'job')['attribute_yes_count'],
        'job_no_count':  get_categorical_chart_data(total_clients, 'job')['attribute_no_count'],
        # marital
        'marital_labels': json.dumps(get_categorical_chart_data(total_clients, 'marital')['labels']),
        'marital_yes_count':  get_categorical_chart_data(total_clients, 'marital')['attribute_yes_count'],
        'marital_no_count':  get_categorical_chart_data(total_clients, 'marital')['attribute_no_count'],
        # education
        'education_labels': json.dumps(get_categorical_chart_data(total_clients, 'education')['labels']),
        'education_yes_count':  get_categorical_chart_data(total_clients, 'education')['attribute_yes_count'],
        'education_no_count':  get_categorical_chart_data(total_clients, 'education')['attribute_no_count'],
        # default
        'default_labels': json.dumps(get_categorical_chart_data(total_clients, 'default')['labels']),
        'default_yes_count':  get_categorical_chart_data(total_clients, 'default')['attribute_yes_count'],
        'default_no_count':  get_categorical_chart_data(total_clients, 'default')['attribute_no_count'],
        # balance
        'balance_labels': get_numeric_chart_data(total_clients, 'balance', decimals=1)['labels'],
        'balance_yes_count': get_numeric_chart_data(total_clients, 'balance', decimals=1)['attribute_yes_count'],
        'balance_no_count': get_numeric_chart_data(total_clients, 'balance', decimals=1)['attribute_no_count'],
        # housing
        'housing_labels': json.dumps(get_categorical_chart_data(total_clients, 'housing')['labels']),
        'housing_yes_count':  get_categorical_chart_data(total_clients, 'housing')['attribute_yes_count'],
        'housing_no_count':  get_categorical_chart_data(total_clients, 'housing')['attribute_no_count'],
        # loan
        'loan_labels': json.dumps(get_categorical_chart_data(total_clients, 'loan')['labels']),
        'loan_yes_count':  get_categorical_chart_data(total_clients, 'loan')['attribute_yes_count'],
        'loan_no_count':  get_categorical_chart_data(total_clients, 'loan')['attribute_no_count'],
        # contact
        'contact_labels': json.dumps(get_categorical_chart_data(total_clients, 'contact')['labels']),
        'contact_yes_count':  get_categorical_chart_data(total_clients, 'contact')['attribute_yes_count'],
        'contact_no_count':  get_categorical_chart_data(total_clients, 'contact')['attribute_no_count'],
        # days (plotted as categorical)
        'day_labels': get_categorical_chart_data(total_clients, 'day')['labels'],
        'day_yes_count': get_categorical_chart_data(total_clients, 'day')['attribute_yes_count'],
        'day_no_count': get_categorical_chart_data(total_clients, 'day')['attribute_no_count'],
        # month
        'month_labels': json.dumps(ordered_month_labels),
        'month_yes_count': get_categorical_chart_data(total_clients, 'month')['attribute_yes_count'],
        'month_no_count': get_categorical_chart_data(total_clients, 'month')['attribute_no_count'],
        # duration
        'duration_labels': get_numeric_chart_data(total_clients, 'duration')['labels'],
        'duration_yes_count': get_numeric_chart_data(total_clients, 'duration')['attribute_yes_count'],
        'duration_no_count': get_numeric_chart_data(total_clients, 'duration')['attribute_no_count'],
        # campaign (plotted as categorical)
        'campaign_labels': get_categorical_chart_data(total_clients, 'campaign')['labels'],
        'campaign_yes_count': get_categorical_chart_data(total_clients, 'campaign')['attribute_yes_count'],
        'campaign_no_count': get_categorical_chart_data(total_clients, 'campaign')['attribute_no_count'],
        # pdays
        'pdays_labels': get_categorical_chart_data(total_clients, 'pdays')['labels'],
        'pdays_yes_count': get_categorical_chart_data(total_clients, 'pdays')['attribute_yes_count'],
        'pdays_no_count': get_categorical_chart_data(total_clients, 'pdays')['attribute_no_count'],
        # previous (plotted as categorical)
        'previous_labels': get_categorical_chart_data(total_clients, 'previous')['labels'],
        'previous_yes_count': get_categorical_chart_data(total_clients, 'previous')['attribute_yes_count'],
        'previous_no_count': get_categorical_chart_data(total_clients, 'previous')['attribute_no_count'],
        # poutcome
        'poutcome_labels': json.dumps(get_categorical_chart_data(total_clients, 'poutcome')['labels']),
        'poutcome_yes_count': get_categorical_chart_data(total_clients, 'poutcome')['attribute_yes_count'],
        'poutcome_no_count': get_categorical_chart_data(total_clients, 'poutcome')['attribute_no_count'],
    })
    

    
    

    
    
    
  
   