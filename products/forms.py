from django import forms
from django.core.exceptions import ValidationError
from datetime import date

class Ticker(forms.Form):
    ticker = forms.CharField(label='股票代碼', initial='0050')
    start_date = forms.DateField(label='開始日期', initial='2020-01-01', widget=forms.DateInput(attrs={'type':'date'}))
    end_date = forms.DateField(label='結束日期', initial=date.today().strftime("%Y-%m-%d"), widget=forms.DateInput(attrs={'type':'date'}))
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data["start_date"]
        end_date = cleaned_data["end_date"]

        if end_date < start_date:
            msg = "開始日期需早於結束日期"
            raise forms.ValidationError(msg)

        today_date = date.today()
        if end_date > today_date:
            msg = "結束日期不應大於今天日期"
            raise forms.ValidationError(msg)
