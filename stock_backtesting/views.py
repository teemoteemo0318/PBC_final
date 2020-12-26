from django.shortcuts import render
import matplotlib.pyplot as plt
import io
import urllib, base64
import mplfinance as mpf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.offline import plot
from plotly.subplots import make_subplots
import requests
from datetime import date
import matplotlib.pyplot as plt
from stock_backtesting import forms, backtest_plot

today = date.today()
# Create your views here.

def stock_backtesting(request):
    form = forms.Portfolio()
    error = None
    graph = None
    if request.method == 'POST':
        form = forms.Portfolio(request.POST)
        if form.is_valid():
            date_list = [form.cleaned_data['date{}'.format(i)] for i in range(1,11) if form.cleaned_data['date{}'.format(i)] != None]
            num_list = [form.cleaned_data['num{}'.format(i)] for i in range(1,11) if form.cleaned_data['num{}'.format(i)] != 0]
            stock_list = [form.cleaned_data['stock{}'.format(i)] for i in range(1,11) if form.cleaned_data['stock{}'.format(i)] != '']
            num_input = len(date_list)

        # 抓這段期間股票的歷史資料
            today = date.today().strftime("%Y-%m-%d")
            url = "https://api.finmindtrade.com/api/v3/data"
            
            price_data = pd.DataFrame()
            price_data['total_profit'] = 0
            # FinMind的API參數設定
            for i in range(num_input):
                sic = stock_list[i]
                num = num_list[i]
                start_date = min(date_list)

                parameter = {
                    "user_id": "r08723058",
                    "password": "tt593842",
                    "dataset": "TaiwanStockPrice",
                    "stock_id": sic,
                    "date": start_date,
                    "end_date": today,
                }

            # 由於在FinMind中，美股及台股的資料格式不同，這邊要分別處理，調整為一致的格式
                resp = requests.get(url, params=parameter)
                data = resp.json()
                data = pd.DataFrame(data["data"])
                df = data[['date','open','max','min','close','Trading_Volume']]
                df['date'] = pd.to_datetime(df['date'])
                df = df.set_index('date')
                df.columns = ['{}_{}'.format(i, sic) for i in ['Open', 'High', 'Low', 'Close', 'Volume']]
                price_data['Close_{}'.format(sic)] = df['Close_{}'.format(sic)]
                price_data['Profit_{}'.format(sic)] = (price_data['Close_{}'.format(sic)] - price_data['Close_{}'.format(sic)].shift(1)) * 1000 * num
                mask = pd.to_datetime(price_data.index) <= pd.to_datetime(date_list[i])
                price_data['Profit_{}'.format(sic)][mask] = 0
                price_data['Profit_{}'.format(sic)] = price_data['Profit_{}'.format(sic)].cumsum()
                price_data['total_profit'] = price_data['total_profit'] + price_data['Profit_{}'.format(sic)]
            
            graph = backtest_plot.plot(price_data, stock_list)

    try:
        error = form.errors.as_data()['__all__'][0]
    except:
        error = None

    return render(request, 'stock_backtesting/base.html',{'form':form, 'error':error, 'graph':graph})