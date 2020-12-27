import plotly.graph_objects as go
import plotly.offline as opy
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

def plot(df, stock_name):
    fig = go.Figure()
    for stock in stock_name:
        fig.add_trace(go.Scatter(x=df.index, y=df['Profit_cumsum_{}'.format(stock)],
                        mode='lines',
                        name=stock))

    fig.add_trace(go.Scatter(x=df.index, y=df['total_cumsum'],
                mode='lines',
                name='total'))
    fig.update_layout(
        title={
            'text': "回測結果",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})
    fig.update_layout(
        xaxis_title="日期",
        yaxis_title="累積損益",
        legend_title="投資標的",
        font=dict(
            size=18,
            color="RebeccaPurple")
    )
    plot_div = opy.plot(fig, auto_open=False, output_type='div')

    return plot_div

def plot_daily_return(df, stock_name):
    fig = go.Figure()
    color = ['red' if i >= 0 else 'green' for i in df.total_daily]
    fig.add_trace(go.Bar(x=df.index, y=df.total_daily, name='單日投組損益', marker_color = color))
    fig.update_layout(
        title={
            'text': "投資組合單日損益",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'})
    fig.update_layout(
        xaxis_title="日期",
        yaxis_title="金額",
        font=dict(
            size=18,
            color="RebeccaPurple")
    )
    plot_div = opy.plot(fig, auto_open=False, output_type='div')
    return plot_div
