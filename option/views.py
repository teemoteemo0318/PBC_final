from django.shortcuts import render
from option import forms
# from option import functions
import io
import urllib, base64
import matplotlib.pyplot as plt

# Create your views here.
def option(request):
    form = forms.OpInfo()
    graph = None

    if request.method == 'POST':
        form = forms.OpInfo(request.POST)

        if form.is_valid():
            start_date = form.cleaned_data['start_date']  # 讀取用戶輸入的開始日期

    try:
        error = form.errors.as_data()['__all__'][0]
    except:
        error = None
    return render(request, 'option/base.html', {'form':form, 'graph':graph, 'error':error})
