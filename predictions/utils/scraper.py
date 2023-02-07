from bs4 import BeautifulSoup
import pandas as pd
import requests

def get_economic_indicators():
    page = requests.get("https://www.moreexchange.cl/tipo-de-cambio-de-divisas-more-exchange/")

    soup = BeautifulSoup(page.text, "html.parser")

    table = soup.find_all("table")
    df_list =  pd.read_html(str(table))
    # print(df_list[0])
    return {
        'dolar': {'bid': df_list[0].loc[0, 'Compra'], 'ask': df_list[0].loc[0, 'Venta']},
        'euro': {'bid': df_list[1].loc[0, 'Compra'], 'ask': df_list[1].loc[0, 'Venta']}
    }




