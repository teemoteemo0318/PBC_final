from django.shortcuts import render
import matplotlib.pyplot as plt
import io
import urllib, base64
from products.models import Stock
import mplfinance as mpf
import pandas as pd
import numpy as np
from products import forms
from products import historical_data_plot, chip_data_plot
import plotly.graph_objects as go
from plotly.offline import plot
from plotly.subplots import make_subplots
import requests
from datetime import date
import matplotlib.pyplot as plt

today = date.today()
# Create your views here.

def products(request):
    form = forms.Ticker()
    info = None
    plot_div = None
    chip = None

    if request.method == 'POST':
        form = forms.Ticker(request.POST)
        
        if form.is_valid():

            # 抓取用戶輸入的資料
            sic = form.cleaned_data['ticker']  # 讀取用戶輸入的股票代碼
            start_date = form.cleaned_data['start_date']  # 讀取用戶輸入的開始日期
            end_date = form.cleaned_data['end_date']  # 讀取用戶輸入的結束日期
            
            # 抓取台股清單
            url = "https://api.finmindtrade.com/api/v3/data"
            parameter = {
                "dataset": "TaiwanStockInfo",
            }
            resp = requests.get(url, params=parameter)
            data = resp.json()
            stock_id = pd.DataFrame(data["data"])

            dataset = "TaiwanStockPrice"
            # 使用FinMind的API
            today = date.today().strftime("%Y-%m-%d")
            url = "https://api.finmindtrade.com/api/v3/data"
            
            # FinMind的API參數設定
            parameter = {
                "user_id": "r08723058",
                "password": "tt593842",
                "dataset": dataset,
                "stock_id": sic,
                "date": start_date,
                "end_date": today,
            }

            # 由於在FinMind中，美股及台股的資料格式不同，這邊要分別處理，調整為一致的格式
            if dataset == "TaiwanStockPrice":
                resp = requests.get(url, params=parameter)
                data = resp.json()
                data = pd.DataFrame(data["data"])
                df = data[['date','open','max','min','close','Trading_Volume']]
                df['date'] = pd.to_datetime(df['date'])
                df = df.set_index('date')
                df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
                df['Volume'] = df['Volume']
                today_close = df.Close.values[-1]
                yesterday_close = df.Close.values[-2]
                df = df[df.index <= pd.to_datetime(end_date)]

            # 畫歷史交易資訊圖
            plot_div = historical_data_plot.historical_pic(df)
            
            # 籌碼資料
            url = "https://api.finmindtrade.com/api/v3/data"
            parameter = {
                "dataset": "InstitutionalInvestorsBuySell",
                "stock_id": sic,
                "date": start_date,
                "end_date": end_date,
            }
            data = requests.get(url, params=parameter)
            data = data.json()
            data = pd.DataFrame(data['data'])
            data['date'] = pd.to_datetime(data['date'])
            data = data.set_index('date')
            
            chip = chip_data_plot.chip_pic(data)

            # 獲得股票的基本資訊
            diff = round(today_close - yesterday_close,2)

            color = 'red' if diff >= 0 else 'green'
            color = 'gray' if diff == 0 else color
            diff = '+' + str(diff) if diff > 0 else str(diff)
            info = {
                'stock_name':stock_id[stock_id['stock_id']==sic].stock_name.values[0],
                'industry':stock_id[stock_id['stock_id']==sic].industry_category.values,
                'sic':sic,
                'today_close': today_close,
                'diff': diff,
                'color': color
            }
    try:
        error = form.errors.as_data()['__all__'][0]
    except:
        error = None
    return render(request, 'products/base.html',{'info':info, 'graph':plot_div, 'form':form, 'chip':chip, 'error':error})

