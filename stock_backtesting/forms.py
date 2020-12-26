from django import forms
from django.core import validators
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from datetime import date
import requests
import pandas as pd

class Portfolio(forms.Form):
    # start_date = forms.DateField(label='開始日期', widget=forms.DateInput(attrs={'type':'date', 'class':'form-label'}))
    # end_date = forms.DateField(label='結束日期', initial=date.today().strftime("%Y-%m-%d"), widget=forms.DateInput(attrs={'type':'date', 'class':'form-label'}))

    stock1 = forms.CharField(label='股票代號1', initial='0050')
    stock2 = forms.CharField(label='股票代號2', required=False)
    stock3 = forms.CharField(label='股票代號3', required=False)
    stock4 = forms.CharField(label='股票代號4', required=False)
    stock5 = forms.CharField(label='股票代號5', required=False)
    stock6 = forms.CharField(label='股票代號6', required=False)
    stock7 = forms.CharField(label='股票代號7', required=False)
    stock8 = forms.CharField(label='股票代號8', required=False)
    stock9 = forms.CharField(label='股票代號9', required=False)
    stock10 = forms.CharField(label='股票代號10', required=False)

    num1 = forms.IntegerField(label='買入數量1', min_value=1, initial=1)
    num2 = forms.IntegerField(label='買入數量2', min_value=0, initial=0, required=False)
    num3 = forms.IntegerField(label='買入數量3', min_value=0, initial=0, required=False)
    num4 = forms.IntegerField(label='買入數量4', min_value=0, initial=0, required=False)
    num5 = forms.IntegerField(label='買入數量5', min_value=0, initial=0, required=False)
    num6 = forms.IntegerField(label='買入數量6', min_value=0, initial=0, required=False)
    num7 = forms.IntegerField(label='買入數量7', min_value=0, initial=0, required=False)
    num8 = forms.IntegerField(label='買入數量8', min_value=0, initial=0, required=False)
    num9 = forms.IntegerField(label='買入數量9', min_value=0, initial=0, required=False)
    num10 = forms.IntegerField(label='買入數量10', min_value=0, initial=0, required=False)

    date1 = forms.DateField(label='買入日期1', widget=forms.DateInput(attrs={'type':'date'}), initial='2020-01-02')
    date2 = forms.DateField(label='買入日期2', widget=forms.DateInput(attrs={'type':'date'}), required=False)
    date3 = forms.DateField(label='買入日期3', widget=forms.DateInput(attrs={'type':'date'}), required=False)
    date4 = forms.DateField(label='買入日期4', widget=forms.DateInput(attrs={'type':'date'}), required=False)
    date5 = forms.DateField(label='買入日期5', widget=forms.DateInput(attrs={'type':'date'}), required=False)
    date6 = forms.DateField(label='買入日期6', widget=forms.DateInput(attrs={'type':'date'}), required=False)
    date7 = forms.DateField(label='買入日期7', widget=forms.DateInput(attrs={'type':'date'}), required=False)
    date8 = forms.DateField(label='買入日期8', widget=forms.DateInput(attrs={'type':'date'}), required=False)
    date9 = forms.DateField(label='買入日期9', widget=forms.DateInput(attrs={'type':'date'}), required=False)
    date10 = forms.DateField(label='買入日期10', widget=forms.DateInput(attrs={'type':'date'}), required=False)


    def clean(self):
        cleaned_data = super().clean()
        date_list = [cleaned_data['date{}'.format(i)] for i in range(1,11)]
        stock_list = [cleaned_data['stock{}'.format(i)] for i in range(1,11)]
        num_list = [cleaned_data['num{}'.format(i)] for i in range(1,11)]
        
        today_date = date.today()

        url = "https://api.finmindtrade.com/api/v3/data"
        parameter = {
            "dataset": "TaiwanStockInfo",
        }
        resp = requests.get(url, params=parameter)
        data = resp.json()
        stock_id = pd.DataFrame(data["data"])
        
        for day in date_list:
            if day != None:
                if day > today_date:
                    msg = "買入日期需早於結束日期"
                    raise forms.ValidationError(msg)

        for stock in stock_list:
            if stock != '':
                if stock not in stock_id['stock_id'].values:
                    msg = "無此股票代碼"
                    raise forms.ValidationError(msg)
        date_list = [i for i in date_list if i != None]
        num_list = [i for i in num_list if i != 0]
        stock_list = [i for i in stock_list if i != '']

        if (len(date_list) != len(stock_list)) or (len(num_list) != len(stock_list)) or (len(date_list) != len(num_list)):
            msg = "肯定是少輸入了什麼"
            raise forms.ValidationError(msg)