def craw_new_data(year,month,date):
    import requests
    import pandas as pd
    from bs4 import BeautifulSoup
    import numpy
    import csv
    import time

            
    info = f'{year}/{month}/{date}'
    url = 'https://www.taifex.com.tw/cht/3/optDailyMarketReport'
    payload = {'queryType':'2',
               'marketCode':'0',
               'dateaddcnt':'',
               'commodity_id':'TXO',
               'commodity_id2':'',
               'MarketCode':'0',
               'commodity_idt':'TXO',
               'commodity_id2t':'',
               'commodity_id2t2':'',
               'queryDate':info
              }
    encoding = 'utf8'
    r = requests.post(url,data=payload)
    r.encoding = encoding
    soup = BeautifulSoup(r.content, 'html.parser')

    data = pd.DataFrame(columns=['契約','到期月份(週別)','履約價','買賣權','開盤價','最高價','最低價','最後成交價','結算價','盤後交易時段成交量','一般交易時段成交量','合計成交量','未沖銷契約量'])
    append_list = {}
    count = 0
    for i in soup.find_all('tr'):
        for j in i.find_all('td',class_ = '12bk'):
            count+=1
            if count > 18:
                if (count-18)%13 == 0:
                    data = data.append(append_list, ignore_index=True)
                    append_list = {}
                    append_list['契約'] = j.text.replace('\n','').replace(' ','').replace('\t','').replace('\r','')
                elif (count-18)%13 == 1:
                    append_list['到期月份(週別)'] = j.text.replace('\n','').replace(' ','').replace('\t','').replace('\r','')
                elif (count-18)%13 == 2:
                    append_list['履約價'] = j.text.replace('\n','').replace(' ','').replace('\t','').replace('\r','')
                elif (count-18)%13 == 3:
                    append_list['買賣權'] = j.text.replace('\n','').replace(' ','').replace('\t','').replace('\r','')
                elif (count-18)%13 == 4:
                    append_list['開盤價'] = j.text.replace('\n','').replace(' ','').replace('\t','').replace('\r','')
                elif (count-18)%13 == 5:
                    append_list['最高價'] = j.text.replace('\n','').replace(' ','').replace('\t','').replace('\r','')
                elif (count-18)%13 == 6:
                    append_list['最低價'] = j.text.replace('\n','').replace(' ','').replace('\t','').replace('\r','')
                elif (count-18)%13 == 7:
                    append_list['最後成交價'] = j.text.replace('\n','').replace(' ','').replace('\t','').replace('\r','')
                elif (count-18)%13 == 8:
                    append_list['結算價'] = j.text.replace('\n','').replace(' ','').replace('\t','').replace('\r','')
                elif (count-18)%13 == 9:
                    append_list['盤後交易時段成交量'] = j.text.replace('\n','').replace(' ','').replace('\t','').replace('\r','')
                elif (count-18)%13 == 10:
                    append_list['一般交易時段成交量'] = j.text.replace('\n','').replace(' ','').replace('\t','').replace('\r','')
                elif (count-18)%13 == 11:
                    append_list['合計成交量'] = j.text.replace('\n','').replace(' ','').replace('\t','').replace('\r','')
                elif (count-18)%13 == 12:
                    append_list['未沖銷契約量'] = j.text.replace('\n','').replace(' ','').replace('\t','').replace('\r','')
    data.to_csv(f'./static/option_data/option_data_{year}_{month}_{date}.csv',index=False,encoding='cp950')
    return data

if __name__ == "__main__":
    craw_new_data(2020,11,11)
