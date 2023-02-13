from django.db import models
from authuser.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator 
import pandas as pd
from .utils.predictor import classification_function 


# Getting the choices for categorical values from pickle file
possible_choices = pd.read_pickle('model/pickle_files/form_input_data.pickle')
column_names = pd.read_pickle('model/pickle_files/input_data_columns.pickle')

""" {'possible_job': ['management', 'technician', 'entrepreneur', 'blue-collar', 'unknown', 'retired', 'admin.', 'services', 'self-employed', 'unemployed', 'housemaid', 'student'], 'possible_marital': ['married', 'single', 'divorced'], 'possible_education': ['primary', 'secondary', 'tertiary', 'unknown'], 'possible_default': ['no', 'yes'], 'possible_housing': ['yes', 'no'], 'possible_loan': ['no', 'yes'], 'possible_contact': ['unknown', 'cellular', 'telephone'], 'possible_month': ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec'], 'possible_poutcome': ['unknown', 'failure', 'other', 'success']} """

job_choices = [(item, item) for item in possible_choices['possible_job']]
marital_choices = [(item, item) for item in possible_choices['possible_marital']]
education_choices = [(item, item) for item in possible_choices['possible_education']]
contact_choices = [(item, item) for item in possible_choices['possible_contact']]
month_choices = [(item, item) for item in possible_choices['possible_month']]
poutcome_choices = [(item, item) for item in possible_choices['possible_poutcome']]


binary_choices = [('yes', 'yes'), ('no', 'no')]



def validate_day(day, month):
    if month == 'feb':
        if day > 29:
            return'f{month} has a maximum of 29 days.'
    elif month in ['apr', 'jun', 'sep', 'nov']:
        if day > 30:
            return f'{month} has a maximum of 30 days.'
    else:
        if day > 31:
            return f'{month} has a maximum of 31 days.'
    return None
    



# Create your models here.
class Client(models.Model):
    full_name = models.CharField(max_length=100)
    age = models.IntegerField()
    job = models.CharField(max_length=100, choices=job_choices)
    marital = models.CharField(max_length=100, choices=marital_choices)
    education = models.CharField(max_length=100, choices=education_choices)
    default = models.CharField(max_length=3, choices=binary_choices)
    balance = models.IntegerField()
    housing = models.CharField(max_length=3, choices=binary_choices)
    loan = models.CharField(max_length=3, choices=binary_choices)
    contact = models.CharField(max_length=100, choices=contact_choices)
    day = models.PositiveSmallIntegerField()
    month = models.CharField(max_length=100, choices=month_choices)
    duration = models.IntegerField()
    campaign = models.IntegerField()
    pdays = models.IntegerField()
    previous = models.IntegerField()
    poutcome = models.CharField(max_length=100, choices=poutcome_choices)
    
    outcome_target = models.CharField(max_length=3, choices=binary_choices, editable=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


    def __str__(self):
        return self.full_name
    
    def clean(self):
        errors = {}
        if self.age < 18 or self.age > 100:
            errors['age'] = 'Age must be higher than 18 and lower than 100.'
        
        day_error = validate_day(self.day, self.month)
        if day_error:
            errors['day'] = day_error
        
        if errors:
            raise ValidationError(errors)
        


    def save(self, *args, **kwargs):
        # Add prediction function
        # self.outcome_target = pred_func(self.age, self.job....)
        data = [[
            self.age,
            self.job,
            self.marital,
            self.education,
            self.default,
            self.balance,
            self.housing,
            self.loan,
            self.contact,
            self.day,
            self.month,
            self.duration,
            self.campaign,
            self.pdays,
            self.previous,
            self.poutcome
        ]]
        input_dataframe = pd.DataFrame(data=data, columns=column_names)
        self.outcome_target = classification_function(input_dataframe)
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'clients'
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'

