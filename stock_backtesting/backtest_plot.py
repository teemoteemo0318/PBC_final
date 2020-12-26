import plotly.graph_objects as go
import plotly.offline as opy
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

def plot(df, stock_name):
    fig = go.Figure()
    for stock in stock_name:
        fig.add_trace(go.Scatter(x=df.index, y=df['Profit_{}'.format(stock)],
                        mode='lines',
                        name=stock))
    def sum_profit(row):
        ans = 0
        for stock in stock_name:
            ans += row['Profit_{}'.format(stock)]
        return ans

    df['total'] = df.apply(sum_profit, axis = 1)
    fig.add_trace(go.Scatter(x=df.index, y=df['total'],
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