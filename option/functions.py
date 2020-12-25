import io
import urllib, base64
import datetime as dt
from bs4 import BeautifulSoup
import time
from option import web_crawler
import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
import mibian
from os import listdir
import math
from scipy import integrate
import requests
import matplotlib.pyplot as plt

def third_wen(y,m):#算當月結算日
    import datetime as dt
    day=21-(dt.date(y,m,1).weekday()+4)%7         #   weekday函數 禮拜一為0;禮拜日為6
    return y,m,day


def get_left_day(year,month,day):
    
    if third_wen(year,month)[2] > day and month != 12:
        left_day_ = dt.date(int(third_wen(year,month)[0]),int(third_wen(year,month)[1]),int(third_wen(year,month)[2])) - dt.date(year,month,day)
    elif third_wen(year,month)[2] > day and month == 12:
        left_day_ = dt.date(int(third_wen(year,month)[0]),int(third_wen(year,month)[1]),int(third_wen(year,month)[2])) - dt.date(year,month,day)
    elif third_wen(year,month)[2] <= day and month != 12:
        left_day_ = dt.date(int(third_wen(year,month+1)[0]),int(third_wen(year,month+1)[1]),int(third_wen(year,month+1)[2])) - dt.date(year,month,day)
    elif third_wen(year,month)[2] <= day and month == 12:
        left_day_ = dt.date(int(third_wen(year+1,1)[0]),int(third_wen(year+1,1)[1]),int(third_wen(year+1,1)[2])) - dt.date(year,month,day)
        
    #print(str(left_day.days))
    return int(str(left_day_.days))

def detect_lastest_data(year,month,date):
    mypath = "./static/option_data/"
    files = listdir(mypath)
    if f'option_data_{year}_{month}_{date}.csv' in files:
        return True
    elif f'option_data_{year}_{month}_{date}.csv' not in files:
        return False


def distr_formula(r,k1,k2,k3,left_day,distance):#johnhull公式
    c1 = float(k1)
    c3 = float(k3)
    c2 = float(k2)
    T = left_day/365
    g = (math.exp(r*T))*(c1  + c3 - 2*c2)/(distance)
    return g


def process_df(year,month,date):#載入資料
    data = pd.read_csv(f'static/option_data/option_data_{year}_{month}_{date}.csv',encoding='cp950')
    #data = data[data['交易時段']!='盤後']
    if third_wen(year,month)[2] > date and month != 12:
        month = str(month).rjust(2,'0')
        data = data[data['到期月份(週別)'] == f'{year}{month}']
        data = data.reset_index()
        del data['index']
    elif third_wen(year,month)[2] <= date and month != 12:
        month = str(month+1).rjust(2,'0')
        data = data[data['到期月份(週別)'] == f'{year}{month}']
        data = data.reset_index()
        del data['index']
    elif third_wen(year,month)[2] <= date and month == 12:
        data = data[data['到期月份(週別)'] == f'{year+1}01']
        data = data.reset_index()
        del data['index']
    #data_process = data[data['Unnamed: 0']== f'{year}/{month}/{date}']
    data_buy = data[data['買賣權']=='Call']
    data_buy = data_buy.reset_index()
    del data_buy['index']
    data_sell = data[data['買賣權']=='Put']
    data_sell = data_sell.reset_index()
    del data_sell['index']
    data_buy['結算價'] = [float(x) for x in data_buy['結算價']]
    data_sell['結算價'] = [float(x) for x in data_sell['結算價']]
    k = data_sell['履約價']
    
    return data_buy,data_sell,k#回傳買權、賣權表格跟K是履約價數列


def get_future_price(year,month,date):#尋找當日小台期貨收盤價
    info = f'{year}/{month}/{date}'
    url = 'https://www.taifex.com.tw/cht/3/futDailyMarketReport'
    payload = {'queryType':'2',
               'marketCode':'0',
                'dateaddcnt':'',
                'commodity_id':'MTX',
                'commodity_id2':'',
                'MarketCode':'0',
                'commodity_idt':'MTX',
                'commodity_id2t':'',
                'commodity_id2t2':'',
                'queryDate':info
                }
    encoding = 'utf8'
    r = requests.post(url,data=payload)
    r.encoding = encoding
    soup = BeautifulSoup(r.content, 'html.parser')
    a = []
    for i in soup.find_all('tr'):
        for j in i.find_all('td',class_ = '12bk'):
            a.append(j.text.replace('\n','').replace('\t','').replace(' ',''))
    print(f'期貨收盤價為{int(a[24])}')
    return int(a[24])

def correct_IV_put(futures_price,data_sell,left_day,k):#修正put的隱波
    IV_sell = []
    for i in range(len(data_sell)):
        try:
            #先用真實價格套入BS模型回推隱波
            a = mibian.BS([futures_price, float(data_sell['履約價'][i]), 0.003, left_day], putPrice= float(data_sell['結算價'][i]))
            IV_sell.append(a.impliedVolatility)
        except:
            pass
    weights_sell = np.polyfit(k, IV_sell, 6)#用6次式回歸修正
    model_sell = np.poly1d(weights_sell)
    b = list(range(min(data_sell['履約價']),max(data_sell['履約價'])+100,100))
    pred_sell = model_sell(b)#套回修正過的回歸式回傳新的隱波
    
    return pred_sell, b#回傳


def correct_IV_call(futures_price,data_buy,left_day,k):#修正call的隱波
    IV_buy = []
    for i in range(len(data_buy)):
        try:
            #先用真實價格套入BS模型回推隱波
            a = mibian.BS([futures_price, float(data_buy['履約價'][i]), 0.003, left_day], callPrice= float(data_buy['結算價'][i]))
            IV_buy.append(a.impliedVolatility)
        except:
            pass
    weights_buy = np.polyfit(pd.to_numeric(k), pd.to_numeric(IV_buy), 6)#用6次式回歸修正
    model_buy = np.poly1d(weights_buy)
    b = list(range(min(data_buy['履約價']),max(data_buy['履約價'])+100,100))
    pred_buy = model_buy(b)#套回修正過的回歸式回傳新的隱波
    
    return pred_buy, b


def predict_call_price(futures_price,data_buy,left_day,k):#修正新的call價格 
    pred_buy, b = correct_IV_call(futures_price,data_buy,left_day,k)#先尋找修正後的call隱波
    whole_buy_price = []
    for i in range(len(b)):
        #用修正後的隱波套入BS模型得到價格並回傳
        call_price = mibian.BS([futures_price,b[i],0.3,left_day],pred_buy[i]).callPrice
        whole_buy_price.append(call_price)
    return whole_buy_price


def predict_put_price(futures_price,data_sell,left_day,k):#修正新的put價格
    pred_sell,b = correct_IV_put(futures_price,data_sell,left_day,k)#先尋找修正後的put隱波
    whole_sell_price = []
    for i in range(len(b)):
        #用修正後的隱波套入BS模型得到價格並回傳
        put_price = mibian.BS([futures_price,b[i],0.3,left_day],pred_sell[i]).putPrice
        whole_sell_price.append(put_price)
    return whole_sell_price


def turn_k_into_return(k,futures_price):#轉換履約價成小台期的報酬率
    a = []
    for i in k:
        a.append(float((i-futures_price)/futures_price))
    return a


def produce_pic(left_day,whole_buy_price,whole_sell_price,k,month,date,futures_price):
    #先來把put_johnhull一下
    r = 0.0003
    k1 = list(whole_sell_price[0:len(whole_sell_price)-2])
    k2 = list(whole_sell_price[1:len(whole_sell_price)-1])
    k3 = list(whole_sell_price[2:len(whole_sell_price)])
    ans1 = []
    for i in range(len(k1)):
        #distance = (k[i+2]-k[i])/2  #抓johnhull的分母
        #print(f'distance:{distance}')
        #if distance == 75:
        #distance = 100
        a = distr_formula(r=r,k1=k1[i],k3=k3[i],k2=k2[i],left_day=left_day,distance=100)
        if a < 0:
            a = 0
        ans1.append(a)
        #print(f'k1:{k1[i]} k2:{k2[i]} k3:{k3[i]}')
        
    #print('----------------')
    
    plt.figure(figsize = (20,10))
    plt.title(f'{month}/{date} put/call mix', fontsize = 25)
    #plt.plot(k,ans1,'s-',color = 'g', label="put_option")
    
    #再把call_johnhull一下
    k1 = list(whole_buy_price[0:len(whole_buy_price)-2])
    k2 = list(whole_buy_price[1:len(whole_buy_price)-1])
    k3 = list(whole_buy_price[2:len(whole_buy_price)])
    ans2 = []
    for i in range(len(k1)):
        #distance = (k[i+2]-k[i])/2
        #print(f'distance:{distance}')
        #if distance == 75:
            #distance = 100
        a = distr_formula(r=r,k1=k1[i],k3=k3[i],k2=k2[i],left_day=left_day,distance=100)
        if a < 0:
            a = 0
        ans2.append(a)
        #print(f'k1:{k1[i]} k2:{k2[i]} k3:{k3[i]}')
    #print('----------------')
        
    #把put跟call兩條作合併，小於當天收盤價用put，大於等於用call
    ans3 = []
    k_ = list(range(min(k)+100, max(k),100))
    #print(k_)
    for i in range(0,len(k_)):
        #print(i)
        if int(k_[i]) < int(futures_price):
            ans3.append(ans1[i])
        elif int(k_[i]) >= int(futures_price):
            ans3.append(ans2[i])
    k_ = turn_k_into_return(k_,futures_price)
    #plt.plot(k_,ans1,'s-',color = 'b', label="mix_option")
    #plt.plot(k_,ans2,'s-',color = 'r', label="mix_option")
    plt.plot(k_,ans3,'s-',color = 'y', label="mix_option")
    # plt.show()
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    return graph


def calculate(year, month, day):
    
    appoint_date = dt.date(int(year), int(month), int(day))
    now = dt.date(int(dt.datetime.now().strftime('%Y-%m-%d-%H').split('-')[0]),int(dt.datetime.now().strftime('%Y-%m-%d-%H').split('-')[1]),int(dt.datetime.now().strftime('%Y-%m-%d-%H').split('-')[2]))
    check_if_ok = appoint_date-now
    
    if int(str((check_if_ok).days)) >= 0:
        now = dt.datetime.now()
        if int(now.strftime('%Y-%m-%d-%H').split('-')[3]) <16:
            now += dt.timedelta(days = -1)
    elif int(str((check_if_ok).days)) < 0:
        now = appoint_date

    weekday = now.weekday()
    if weekday == 5:
        now += dt.timedelta(days = -1)
    elif weekday == 6:
        now += dt.timedelta(days = -2)
    else:
        pass


    time_line = now.strftime('%Y-%m-%d').split('-')
    year = int(time_line[0])
    month = int(time_line[1])
    date_ = int(time_line[2])

    if not detect_lastest_data(year, month, date_):
        web_crawler.craw_new_data(year,month,date_)
    else:
        pass
    print('執行process_df')
    data_buy, data_sell, k = process_df(year,month,date_)
    print('執行get_future_price')
    futures_price = get_future_price(year,month,date_)
    print('執行get_left_day')
    left_day = get_left_day(year,month,date_)
    print('執行predict_call_price')
    whole_buy_price = predict_call_price(futures_price,data_buy,left_day,k)
    print('執行predict_put_price')
    whole_sell_price = predict_put_price(futures_price,data_sell,left_day,k)
    print('執行produce_pic')
    graph = produce_pic(left_day,whole_buy_price,whole_sell_price,k,month,date_,futures_price)
    return graph