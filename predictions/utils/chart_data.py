import pandas as pd
import numpy as np
import json


def get_numeric_chart_data(clients, client_attribute, decimals=0):
    # Can't generate the labels with less than 2 clients, so this condition is added
    if len(clients) < 2:
        return {
            'labels': [0, 100],
            'attribute_yes_count': [0, 0],
            'attribute_no_count': [0, 0]
        }
    # Saves in different variables clients that will and won't take the term deposit
    yes_clients = clients.filter(outcome_target='yes')
    no_clients = clients.filter(outcome_target='no')
    
    # Gets the attributes for each client to generate the range of the data for the charts
    total_attributes = [getattr(client, client_attribute) for client in clients]
    max_value = max(total_attributes)
    min_value = min(total_attributes)
    number_of_bins = 10
    
    # Generates the bins and labels for the pd.cut function
    bins = np.linspace(min_value, max_value, number_of_bins)
    labels = np.linspace(bins[1], max_value, number_of_bins - 1)

    # Gets the attributes for yes and no clients and generates a label column to be used in the charts
    yes_attributes = [getattr(client, client_attribute) for client in yes_clients]
    yes_df = pd.DataFrame(yes_attributes, columns=[client_attribute])
    yes_df['label'] = pd.cut(x=yes_df[client_attribute], bins=bins, labels=labels, include_lowest=True)
    yes_count = yes_df['label'].value_counts().sort_index()

    no_attributes = [getattr(client, client_attribute) for client in no_clients]
    no_df = pd.DataFrame(no_attributes, columns=[client_attribute])
    no_df['label'] = pd.cut(x=no_df[client_attribute], bins=bins, labels=labels, include_lowest=True)
    no_count = no_df['label'].value_counts().sort_index()

    return {
        'labels': [round(label, decimals) for label in list(labels)],
        'attribute_yes_count': list(yes_count.values),
        'attribute_no_count': list(no_count.values)
    }




def get_categorical_chart_data(clients, client_attribute):
    # Can't generate the labels with less than 2 clients, so this condition is added
    if len(clients) < 2:
        return {
            'labels': [0, 100],
            'attribute_yes_count': [0, 0],
            'attribute_no_count': [0, 0]
        }
    
    # Saves in different variables clients that will and won't take the term deposit
    yes_clients = clients.filter(outcome_target='yes')
    no_clients = clients.filter(outcome_target='no')

    # Gets the unique labels for the client list
    labels = [getattr(client, client_attribute) for client in clients]
    unique_labels = np.unique(labels)
    
    # Generates a dictionary with eacth attribute starting at 0, the count is the increasing with eacth repetition.
    yes_attributes = [getattr(client, client_attribute) for client in yes_clients]
    yes_dictionary = {key: 0 for key in unique_labels}
    
    for attribute in yes_attributes:
        yes_dictionary[attribute] += 1
    
   
    # Generates a dictionary with eacth attribute starting at 0, the count is the increasing with eacth repetition.
    no_attributes = [getattr(client, client_attribute) for client in no_clients]
    no_dictionary = {key: 0 for key in unique_labels}
    
    for attribute in no_attributes:
        no_dictionary[attribute] += 1 
    
    
    return {
        'labels': list(unique_labels),
        'attribute_yes_count': list(yes_dictionary.values()),
        'attribute_no_count': list(no_dictionary.values())
    }
