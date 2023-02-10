import pandas as pd
""" test_input_dict = {'age': 58, 'job': 'management', 'marital': 'married', 'education': 'tertiary', 'default': 'no', 'balance': 2143, 'housing': 'yes', 'loan': 'no', 'contact': 'unknown', 'day': 5, 'month': 'may', 'duration': 261, 'campaign': 1, 'pdays': -1, 'previous': 0, 'poutcome': 'unknown'}


values = [[value for value in test_input_dict.values()]]
columns = test_input_dict.keys()
test_input = pd.DataFrame(data=values, columns=columns) """



def classification_function(input_df):

    numbers_scaler = pd.read_pickle('model/pickle_files/numbers_scaler.pickle')
    text_encoders = pd.read_pickle('model/pickle_files/text_encoders.pickle')
    selected_model = pd.read_pickle('model/pickle_files/selected_model.pickle')

    # Separating text and number columns
    input_data_numbers = input_df.select_dtypes(include='number')
    input_data_text = input_df.select_dtypes(include='object')
    # Scaling the numbers
    input_data_numbers_scaled = pd.DataFrame(data=numbers_scaler.transform(input_data_numbers), columns=input_data_numbers.columns)
    # Text processing
    input_data_text_encoded = pd.DataFrame()
    for index, encoder in enumerate(text_encoders):
        column_name = input_data_text.columns[index]
        input_data_text_encoded[column_name] = encoder.fit_transform(input_data_text.iloc[:, index])
    # Concatenating text and numbers
    input_data_preprocessed = pd.concat([input_data_numbers_scaled, input_data_text_encoded], axis=1)
    # Prediction
    prediction = selected_model.predict(input_data_preprocessed)

    

    if prediction[0] == 0:
        return 'no'
    else:
        return 'yes'



