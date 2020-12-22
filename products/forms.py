from django import forms

class Ticker(forms.Form):
    ticker = forms.CharField(label='股票代碼')
    start_date = forms.DateField(label='開始日期', widget=forms.DateInput(attrs={'type':'date'}))
    end_date = forms.DateField(label='結束日期', widget=forms.DateInput(attrs={'type':'date'}))
