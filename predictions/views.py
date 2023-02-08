from django.shortcuts import render
from .utils.scraper import get_economic_indicators 

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