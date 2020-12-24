from django.shortcuts import render
from tx import forms
from tx import functions
import io
import urllib, base64
import matplotlib.pyplot as plt

# Create your views here.
def tx(request):
    form = forms.BackTestForm()
    graph = None
    plot_div = None
    if request.method == 'POST':
        form = forms.BackTestForm(request.POST)

        if form.is_valid():
            start_date = form.cleaned_data['start_date']  # 讀取用戶輸入的開始日期
            end_date = form.cleaned_data['end_date']  # 讀取用戶輸入的結束日期
            ma_filter = form.cleaned_data['ma_filter']
            up_down_filter = form.cleaned_data['up_down_filter']
            ma_filter_len = form.cleaned_data['ma_filter_len']
            holding_day = form.cleaned_data['holding_day']
            plot_div, graph = functions.calculate(start_date, end_date, ma_filter, up_down_filter, ma_filter_len, holding_day)
    try:
        error = form.errors.as_data()['__all__'][0]
    except:
        error = None
    return render(request, 'tx/base.html', {'form':form, 'graph':graph, 'plot_div':plot_div, 'error':error})
