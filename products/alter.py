# 這裡放的是替代用的畫圖函數及其參考資料

# mpl-finance
# https://github.com/matplotlib/mplfinance/blob/master/examples/addplot.ipynb

# buffer = io.BytesIO()
# mpf.plot(df, type='candle', volume=True, savefig=buffer)
# buffer.seek(0)
# image_png = buffer.getvalue()
# buffer.close()
# graphic = base64.b64encode(image_png)
# graphic = graphic.decode('utf-8')
# return render(request, 'products/base.html',{'graphic':graphic})


# maplotlib
# https://stackoverflow.com/questions/61936775/how-to-pass-matplotlib-graph-in-django-template
# fig, (ax1,ax2) = plt.subplots(nrows=2, ncols=1, sharex=True,figsize=(20,8))
# ax1.plot(dates, highs)
# ax2.bar(dates, volumes)
# buffer = io.BytesIO()
# fig.savefig(buffer, format='png')
# buffer.seek(0)
# image_png = buffer.getvalue()
# buffer.close()
# graphic = base64.b64encode(image_png)
# graphic = graphic.decode('utf-8')
# return render(request, 'products/base.html',{'graphic':graphic})

# import plotly.graph_objects as go
# import plotly.offline as opy
# # https://stackoverflow.com/questions/36846395/embedding-a-plotly-chart-in-a-django-template
# figure = go.Figure(data=[go.Candlestick(x=df.index,
#             open=df['Open'],
#             high=df['High'],
#             low=df['Low'],
#             close=df['Close'])])
# plot_div = opy.plot(figure, auto_open=False, output_type='div')
# return render(request, 'products/base.html',{'graph':plot_div})

    # 使用自己建的資料庫
    # stock = Stock.objects.filter(company=sic).order_by('date')
    # opens = []
    # highs = []
    # lows = []
    # closes = []
    # volumes = []
    # dates = []
    # for data in stock:
    #     opens.append(data.open)
    #     highs.append(data.high)
    #     lows.append(data.low)
    #     closes.append(data.close)
    #     volumes.append(data.volume)
    #     dates.append(data.date)
    # df = pd.DataFrame()
    # df.index.name = 'Date'
    # df['Open'] = opens
    # df['High'] = highs
    # df['Low'] = lows
    # df['Close'] = closes
    # df['Volume'] = volumes
    # df.index = dates
    # df.index = pd.to_datetime(df.index)

    # figure = go.Figure(data=[go.Candlestick(x=df.index,
    #             open=df['Open'],
    #             high=df['High'],
    #             low=df['Low'],
    #             close=df['Close'])])


    # https://chart-studio.plotly.com/~jackp/17421/plotly-candlestick-chart-in-python/#/