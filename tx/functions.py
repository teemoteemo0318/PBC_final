import datetime
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import io
import urllib, base64
from django.conf import settings
import requests
from datetime import date
# plt.style.use('seaborn')

def calculate(start_date, end_date, ma_filter, up_down_filter, ma_filter_len=1, holding_day=1):
    startdatetime = pd.to_datetime(start_date)
    enddatetime = pd.to_datetime(end_date)
    # start_year = start_date.year
    # start_month = start_date.month
    # start_day = start_date.day
    # end_year = end_date.year
    # end_month = end_date.month
    # end_day = end_date.day
    moving_avg_updown = int(ma_filter)  #0不篩選 1為篩選收均線以上 -1為篩選收均線以下
    up_down = int(up_down_filter)  # 0不篩選漲跌, 1為篩上漲, 2為篩下跌 
    moving_avg = int(ma_filter_len)
    holddays = int(holding_day)

    url = "https://api.finmindtrade.com/api/v3/data"
    parameter = {
        "dataset": "TaiwanStockPrice",
        "stock_id": "TAIEX",
        "date": "2001-01-01",
        "end_date": date.today().strftime("%Y-%m-%d"),
    }
    resp = requests.get(url, params=parameter)
    data = resp.json()
    data = pd.DataFrame(data["data"])
    data['date'] = pd.to_datetime(data['date'])
    data = data.drop(columns=['stock_id', 'Trading_money', 'spread', 'Trading_turnover'])
    data = data[['date', 'open', 'max', 'min', 'close', 'Trading_Volume']]
    data.columns = ['Date','Open','High','Low','Close','Volume']
    data["datetime"] = data['Date'] # 日期
    data['moving_avg']=0 # 均線的價格
    data['moving_avg_updown']=0 # 收盤在該均線上或下
    data['up_down'] = 0 # 當日漲或跌
    data['end_price'] = 0  # 持有到結束時的收盤價
    data['return_percent'] = 0 # 報酬率

    def on_avg(row):
        ans = 0
        if row['Close'] > row['moving_avg']:
            ans = 1
        elif row['Close'] < row['moving_avg']:
            ans = -1
        return ans


    def on_avg_ud(row):
        ans = 0
        if row['Close'] > row['Close_lag1']:
            ans = 1
        elif row['Close'] < row['Close_lag1']:
            ans = 2
        return ans

    data['moving_avg'] = data['Close'].rolling(moving_avg).mean()
    data['moving_avg_updown'] = data.apply(on_avg, axis=1)
    data['Close_lag1'] = data['Close'].shift(1)
    data['up_down'] = data.apply(on_avg_ud, axis=1)
    data = data.drop(columns=['Close_lag1'])
    data['end_price'] = data['Close'].shift(-holddays)
    data['return_percent'] = 100 * (data['end_price'] - data['Close']) / data['Close']
    # for i in range(0, data.shape[0]):  # 讀取資料 填入欄位資料：日期 均線平均 均線上下 持有到到期價格等
        # data.loc[i, 'datetime'] = datetime.datetime.strptime(data.loc[i][0],"%Y/%m/%d")
        # if i >= moving_avg-1:
            # sum_temp = 0
            # for j in range(moving_avg):
            #     sum_temp += data.loc[i-j,'Close']
            # if moving_avg != 0:
            #     data.loc[i, 'moving_avg'] = sum_temp/moving_avg

            # if  data.loc[i,'Close'] > data.loc[i, 'moving_avg']:
            #     data.loc[i, 'moving_avg_updown'] = 1
            # elif data.loc[i,'Close'] < data.loc[i, 'moving_avg']:
            #     data.loc[i, 'moving_avg_updown'] = -1

        # if i > 0:
        #     if data.loc[i,'Close'] > data.loc[i-1,'Close']:
        #         data.loc[i, 'up_down'] = 1
        #     elif data.loc[i,'Close'] < data.loc[i-1,'Close']:
        #         data.loc[i, 'up_down'] = 2

        # if i+holddays < data.shape[0]:
            # data.loc[i, 'end_price'] = data.loc[i+holddays,'Close']
            # data.loc[i, 'return_percent'] = 100* ((data.loc[i, 'end_price'] - data.loc[i,'Close'])/data.loc[i,'Close'])
    # print(sum(data['up_down2'] != data['up_down']))
    # print(sum(data['end_price2'] != data['end_price']))
    # print(sum(data['return_percent2'] != data['return_percent']))
    # data.to_csv('test.csv')
    # temp0 = 0
    # temp1 = 0
    # temp2 = 0
    # temp3 = data.shape[0]
    data0 = []
    data1 = []
    data2 = []
    data3 = []

    # 取得設定的開始及結束日期內的資料
    # for i in range(0,data.shape[0]):
    #     if temp0 == 0:
    #         if (data.loc[i,'datetime']-startdatetime).days>=0:
    #             temp0 = 1
    #             temp2 = i
    #             #data0 = data[i:]
    #     if temp0 == 1 and temp1 == 0:
    #         if (data.loc[i,'datetime']-enddatetime).days>0:
    #             temp1 = 1
    #             temp3 = i
    # time_mask = (data['datetime'] >= startdatetime) and (data['datatime'] <= enddatetime)
    data0 = data[(data['datetime'] >= startdatetime) & (data['datetime'] <= enddatetime)]
    # data0 = data[temp2:temp3]


    # 取得要的濾網及漲跌資料
    if up_down != 0:
        data1 = data0[data0["up_down"]==up_down]
    else:
        data1 = data0

    if moving_avg_updown != 0:
        data2 = data1[data1["moving_avg_updown"]==moving_avg_updown]
    else:
        data2 = data1

    data3 = data2[data2["end_price"]!=0] 

    if len(data3)>=1:

        return_count  = list(data3['return_percent'].to_numpy())

        import math
        tmp = data3['return_percent'].describe()
        tmp['skew'] = data3['return_percent'].skew()
        tmp['kurtosis'] = data3['return_percent'].kurtosis()


        # 以下數行為輸出敘述統計量資料
        import plotly.graph_objects as go
        df = pd.DataFrame()
        df['Statistics'] = tmp.index
        df['value'] = tmp.values
        df = df.round(4)
        table = go.Figure(data=[go.Table(
            header=dict(values=list(df.columns),
                        fill_color='#3474eb',
                        align='left',
                        font=dict(color='white', size=12)),
            cells=dict(values=[df['Statistics'], df.value],
                    fill_color='lavender',
                    align='left'))
        ])
        import plotly.offline as opy
        table.update_layout(width=400, height=500)
        plot_div = opy.plot(table, auto_open=False, output_type='div')

        endpoints = []

        # 以下數行轉換長條圖到折線位置上
        for i in range(int(10*data3['return_percent'].min())-1, int(10*data3['return_percent'].max())+1, 1):
            endpoints.append(i/10)

        n, bins, _ = plt.hist(return_count, bins = endpoints, density=1, facecolor = "gray", edgecolor = "black")
        plt.cla()
        n = n/10

        bins2 = []
        for i in range(len(bins)-1):
            bins2.append((bins[i]+bins[i+1])/2)


        # 以下數行為輸出結果的折線圖

        plt.plot(bins2, n) 
        plt.xlabel("Return (percent)")
        plt.ylabel("Probability")
        plt.title("Probability Function")
        plt.xlim(data3['return_percent'].min()-0.1, data3['return_percent'].max()+0.1) # 要顯示的範圍(報酬百分比)
        plt.ylim(0)
        ax = plt.gca()
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        graph = base64.b64encode(image_png)
        graph = graph.decode('utf-8')
        return plot_div, graph
    else:
        print('符合回測條件的開盤天數為0')