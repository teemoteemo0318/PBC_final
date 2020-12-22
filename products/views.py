from django.shortcuts import render
import matplotlib.pyplot as plt
import io
import urllib, base64
from products.models import Stock
import mplfinance as mpf
import pandas as pd
import numpy as np
from products import forms
from products import functions
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


    if request.method == 'POST':
        form = forms.Ticker(request.POST)
        if form.is_valid():
            # 抓取用戶輸入的資料
            sic = form.cleaned_data['ticker']  # 讀取用戶輸入的股票代碼
            start_date = form.cleaned_data['start_date']  # 讀取用戶輸入的開始日期
            end_date = form.cleaned_data['end_date']  # 讀取用戶輸入的結束日期
            
            # 抓取美股清單列表
            url = 'https://api.finmindtrade.com/api/v3/data?dataset=USStockInfo'
            data = requests.get(url)
            data = data.json()
            data = pd.DataFrame(data['data'])
            us_stock_id = data['stock_id'].unique()
            
            # 判斷是美股還台股，選擇要抓的資料集
            if sic in us_stock_id:
                dataset = "USStockPrice"
            else:
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
                "end_date": end_date,
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

            elif dataset == "USStockPrice":
                data = requests.get(url, params=parameter)
                data = data.json()
                data = pd.DataFrame(data['data'])
                df = data[['date', 'Open', 'High', 'Low', 'Close', 'Volume']]
                df['date'] = pd.to_datetime(df['date'])
                df = df.set_index('date')
            plot_div = functions.historical_pic(df) # 根據抓到的資料畫圖
            
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
            name = data.name.unique()
            data['date'] = pd.to_datetime(data['date'])
            data = data.set_index('date')
            
            fig = make_subplots(rows=5, cols=1, subplot_titles=['合計', '自營商避險', '自營商自行買賣', '外資', '投信'])
            name = data.name.unique()[[0,1,3,4]]
            buy_sum = data.groupby('date')['buy'].sum()
            sell_sum = data.groupby('date')['sell'].sum()
            fig.add_trace(go.Scatter(x=buy_sum.index, y=(buy_sum.values-sell_sum.values)/1000, name='三大法人合計淨買', mode='lines', line=dict(color='gray', width=1)), row=1, col=1)
            fig.add_trace(go.Bar(x=buy_sum.index, y=buy_sum.values/1000, name='三大法人合計買', marker_color='red'), row=1, col=1)
            fig.add_trace(go.Bar(x=sell_sum.index, y=-sell_sum.values/1000, name='三大法人合計賣', marker_color='green'), row=1, col=1)
            for i, obj in enumerate(name):
                df = data[data['name']==obj]
                fig.add_trace(go.Scatter(x=df.index, y=(df.buy-df.sell)/1000, name='{} 淨買'.format(obj), mode='lines', line=dict(color='gray', width=1)), row=i+2, col=1)
                fig.add_trace(go.Bar(x=df.index, y=df.buy/1000, name='{} buy'.format(obj),marker_color='red'), row=i+2, col=1)
                fig.add_trace(go.Bar(x=df.index, y=-df.sell/1000, name='{} sell'.format(obj), marker_color='green'), row=i+2, col=1)
            fig.update_layout(showlegend=False)
            fig.update_layout(height=800, width=1200, title_text="三大法人")
            chip = plot(fig, output_type='div')

            return render(request, 'products/base.html',{'graph':plot_div, 'form':form, 'chip':chip})
    return render(request, 'products/base.html', {'form':form, 'date':date})

