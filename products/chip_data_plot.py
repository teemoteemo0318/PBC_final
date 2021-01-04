from django.shortcuts import render
import matplotlib.pyplot as plt
import io
import urllib, base64
from products.models import Stock
import mplfinance as mpf
import pandas as pd
import numpy as np
from products import forms
from products import historical_data_plot
import plotly.graph_objects as go
from plotly.offline import plot
from plotly.subplots import make_subplots
import requests
from datetime import date
import matplotlib.pyplot as plt

def chip_pic(data):
    '''
    input : df with buy, sell, date, name

    output :　三大法人買進及賣出的量的圖
    '''

    # 建立五張子圖
    fig = make_subplots(rows=5, cols=1, shared_xaxes=True, subplot_titles=['合計', '自營商避險', '自營商自行買賣', '外資', '投信'])
    
    name = data.name.unique()[[0,1,3,4]]  # 是三大法人中的哪一個
    
    # 計算三大法人合計買及賣
    buy_sum = data.groupby('date')['buy'].sum()  # 三大法人合計買入
    sell_sum = data.groupby('date')['sell'].sum()  # 三大法人合計賣出

    # 將三大法人合計買賣作圖，放入圖一
    fig.add_trace(go.Scatter(x=buy_sum.index, y=(buy_sum.values-sell_sum.values)/1000, name='三大法人合計淨買', mode='lines', line=dict(color='gray', width=1)), row=1, col=1)
    fig.add_trace(go.Bar(x=buy_sum.index, y=buy_sum.values/1000, name='三大法人合計買', marker_color='red'), row=1, col=1)
    fig.add_trace(go.Bar(x=sell_sum.index, y=-sell_sum.values/1000, name='三大法人合計賣', marker_color='green'), row=1, col=1)
    
    # 針對單一法人歷史買賣作圖
    for i, obj in enumerate(name):
        df = data[data['name']==obj]  # 擷取此法人的買賣資料
        fig.add_trace(go.Scatter(x=df.index, y=(df.buy-df.sell)/1000, name='{} 淨買'.format(obj), mode='lines', line=dict(color='gray', width=1)), row=i+2, col=1)
        fig.add_trace(go.Bar(x=df.index, y=df.buy/1000, name='{} buy'.format(obj),marker_color='red'), row=i+2, col=1)
        fig.add_trace(go.Bar(x=df.index, y=-df.sell/1000, name='{} sell'.format(obj), marker_color='green'), row=i+2, col=1)
    
    # 關閉圖標顯示
    fig.update_layout(showlegend=False)
    # 長寬、標題設定
    fig.update_layout(height=800, width=1000, title_text="三大法人")
    # 圖片輸出
    chip = plot(fig, output_type='div')
    return chip