from django import forms
from django.core.exceptions import ValidationError

class Ticker(forms.Form):
    ticker = forms.CharField(label='股票代碼')
    start_date = forms.DateField(label='開始日期', widget=forms.DateInput(attrs={'type':'date'}))
    end_date = forms.DateField(label='結束日期', widget=forms.DateInput(attrs={'type':'date'}))
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data["start_date"]
        end_date = cleaned_data["end_date"]

        if end_date < start_date:
            msg = "End date should be greater than start date."
            raise forms.ValidationError(msg)
