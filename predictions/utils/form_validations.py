def validate_age(age):
    if age < 18:
            return 'Age must be higher than 18.'
    elif age > 100:
        return 'Age must be lower than 100.'
    else:
        return None


def validate_day(day, month):
    if day < 1:
        return 'Minimum day must be 1.'
    
    elif month == 'feb':
        if day > 29:
            return'f{month} has a maximum of 29 days.'
    elif month in ['apr', 'jun', 'sep', 'nov']:
        if day > 30:
            return f'{month} has a maximum of 30 days.'
    else:
        if day > 31:
            return f'{month} has a maximum of 31 days.'
    return None

def validate_duration(time):
    if time < 0:
        return 'Choose a value equal or higher than 0.'
    else:
        return None
    
def validate_campaign(number):
    if number < 0:
        return 'Choose a value equal or higher than 0.'
    else:
        return None
    
def validate_pdays(number):
    if number < -1:
        return 'Choose a value equal or higher than -1.'
    else:
        return None
    
def validate_previous(number):
    if number < 0:
        return 'Choose a value equal or higher than 0.'
    else:
        return None