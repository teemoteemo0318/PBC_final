from django import forms
from django.core import validators
from django.core.exceptions import ValidationError


class BackTestForm(forms.Form):
    start_date = forms.DateField(label='開始日期', widget=forms.DateInput(attrs={'type':'date'}))
    end_date = forms.DateField(label='結束日期', widget=forms.DateInput(attrs={'type':'date'}))
    up_down_filter_choice = (
        (0, '不須漲跌濾網'),
        (1, '當日漲'),
        (2, '當日跌'),
    )
    up_down_filter = forms.ChoiceField(label='當日漲跌濾網', choices = up_down_filter_choice)
    ma_filter_choice = (
        (0, '不須均線濾網'),
        (1, '收均線以上'),
        (-1, '收均線以下'),
    )
    ma_filter = forms.ChoiceField(label='均線濾網', choices = ma_filter_choice) 
    ma_filter_len = forms.IntegerField(label='均線濾網長度', min_value=1)
    holding_day = forms.IntegerField(label='持有天數', min_value=1)

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        if end_date <= start_date:
            raise ValidationError({
                        'end_date': ValidationError("結束日期須晚於開始日期")})