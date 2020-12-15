from django import forms

class Ticker(forms.Form):
    ticker = forms.CharField()
    