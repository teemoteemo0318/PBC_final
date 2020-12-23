from django.shortcuts import render
from tx import forms
from tx import functions
import io
import urllib, base64
import matplotlib.pyplot as plt

# Create your views here.
def tx(request):
    if request.method == 'POST':
        form = forms.BackTestForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']  # 讀取用戶輸入的開始日期
            end_date = form.cleaned_data['end_date']  # 讀取用戶輸入的結束日期
            ma_filter = form.cleaned_data['ma_filter']
            up_down_filter = form.cleaned_data['up_down_filter']
            ma_filter_len = form.cleaned_data['ma_filter_len']
            holding_day = form.cleaned_data['holding_day']
            graph = functions.calculate(start_date, end_date, ma_filter, up_down_filter, ma_filter_len, holding_day)
            # fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, sharex=True,figsize=(20,8))
            # n, bins, _ = ax1.hist(reture_count, bins = endpoints, density=1, facecolor = "gray", edgecolor = "black")
            # n = n/10
            # bins2 = []
            # for i in range(len(bins)-1):
            #     bins2.append((bins[i]+bins[i+1])/2)

            # # 以下數行為輸出結果的折線圖
            # ax2.plot(bins2, n) 
            # ax2.xlabel("Reture (percent)")
            # ax2.ylabel("Probability")
            # ax2.title("Probability Function")
            # ax2.xlim(data3['reture_percent'].min(), data3['reture_percent'].max()) # 要顯示的範圍(報酬百分比)
            # ax2.ylim(0)
        
            # buffer = io.BytesIO()
            # fig.savefig(buffer, format='png')
            # buffer.seek(0)
            # image_png = buffer.getvalue()
            # buffer.close()
            # graph = base64.b64encode(image_png)
            # graph = graph.decode('utf-8')
        # else:
        #     pass
    else:
        form = forms.BackTestForm()
        graph = None
    return render(request, 'tx/base.html', {'form':form, 'graph':graph})
