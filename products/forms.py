from django import forms

class Ticker(forms.Form):
    ticker = forms.CharField(label='請輸入股票代碼')
    