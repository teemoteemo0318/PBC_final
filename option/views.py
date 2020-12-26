from django.shortcuts import render
from option import forms
from option import functions
import io
import urllib, base64
import matplotlib.pyplot as plt

# Create your views here.
def option(request):
    form = forms.OpInfo()
    graph = None
    error = None
    if request.method == 'POST':
        form = forms.OpInfo(request.POST)

        if form.is_valid():
            start_date = form.cleaned_data['start_date']  # 讀取用戶輸入的開始日期
            year, month, day = start_date.year, start_date.month, start_date.day
            
            try:
                graph = functions.calculate(year, month ,day)
            except:
                error = '發生未知的錯誤，請檢查logs'

    try:
        error = form.errors.as_data()['__all__'][0]
    except:
        pass
    return render(request, 'option/base.html', {'form':form, 'graph':graph, 'error':error})
