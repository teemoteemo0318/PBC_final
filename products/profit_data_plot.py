import plotly.graph_objects as go
import plotly.offline as opy
import pandas as pd
import numpy as np
import os

def profic_pic(ticker):
    df = get_monthly_profit(ticker)
    fig = go.Figure([go.Bar(x=df.index, y=df['monthly profit'],)])
    fig.update_layout(
        title='{} 每月營收'.format(ticker),
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="RebeccaPurple"
        )
    )
    # 將畫圖結果輸出
    plot_div = opy.plot(fig, auto_open=False, output_type='div')

    return plot_div

def get_monthly_profit(ticker):
    main_dir = os.path.join('products/data', 'monthly_report')
    files = os.listdir(main_dir)
    result = pd.DataFrame()
    profit_list = []
    date_list = []
    for file in files:
        if '.csv' not in file:
            continue
        _, _, year, month = file.replace('.csv', '').split('_')
        df = pd.read_csv(os.path.join(main_dir, 'monthly_report_{}_{}.csv'.format(year, month)))
        profit = df[df['公司代號'] == ticker]['當月營收'].values[0]
        time = '{}-{}'.format(1911+int(year), month)
        profit_list.append(profit)
        date_list.append(time)
    result['date'] = date_list
    result['monthly profit'] = profit_list
    result['date'] = pd.to_datetime(result['date'])
    result = result.set_index('date')
    result = result.sort_index()
    return result






