from django import forms
from django.core import validators
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from datetime import date

class OpInfo(forms.Form):
    start_date = forms.DateField(label='開始日期', widget=forms.DateInput(attrs={'type':'date', 'class':'form-label'}))
    # end_date = forms.DateField(label='結束日期', initial=date.today().strftime("%Y-%m-%d"), widget=forms.DateInput(attrs={'type':'date', 'class':'form-label'}))


    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data["start_date"]


        today_date = date.today()
        if start_date > today_date:
            msg = "開始日期需早於結束日期"
            raise forms.ValidationError(msg)