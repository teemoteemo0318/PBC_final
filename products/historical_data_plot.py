import plotly.graph_objects as go
import plotly.offline as opy
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
# import plotly.graph_objs as go 


# https://chart-studio.plotly.com/~jackp/17421/plotly-candlestick-chart-in-python/#/

# 畫個股歷史交易資訊
def historical_pic(df):
    '''
    input : df with Open, High, Low, Close, Volume

    output : historical price plot
    '''


    INCREASING_COLOR = '#cf1717'  # 設定上漲時的顏色
    DECREASING_COLOR = '#138f36'  # 設定下跌時的顏色

    # 整理要畫圖的個股的歷史資訊
    data = [ dict(
            type = 'candlestick',
            open = df.Open,
            high = df.High,
            low = df.Low,
            close = df.Close,
            x = df.index,
            yaxis = 'y2',
            name = 'OHLC',
            increasing = dict( line = dict( color = INCREASING_COLOR ) ),
            decreasing = dict( line = dict( color = DECREASING_COLOR ) ),
        ) ]

    layout=dict()

    # 設定圖的長寬等基本資訊
    fig = dict( data=data, layout=layout )
    fig['layout'] = dict()
    fig['layout']['hovermode'] = "x unified"
    fig['layout']['plot_bgcolor'] = 'rgb(250, 250, 250)'
    fig['layout']['height'] = 500
    fig['layout']['width'] = 1000
    fig['layout']['xaxis'] = dict( rangeselector = dict( visible = True ) )
    fig['layout']['yaxis'] = dict( domain = [0, 0.2], showticklabels = False, fixedrange = False)
    fig['layout']['yaxis2'] = dict( domain = [0.2, 0.8])
    fig['layout']['legend'] = dict( orientation = 'h', y=0.9, x=0.3, yanchor='bottom' )
    fig['layout']['margin'] = dict( t=40, b=40, r=40, l=40 )



    # 增加調整時間窗格的按鈕
    # source : https://plotly.com/python/range-slider/
    rangeselector=dict(
        visible = True,
        x = 0, y = 0.9,
        bgcolor = 'rgba(150, 200, 250, 0.4)',
        font = dict( size = 13 ),
        buttons=list([
            dict(count=1,
                label='reset',
                step='all'),
            dict(count=1,
                label='1yr',
                step='year',
                stepmode='backward'),
            dict(count=3,
                label='3 mo',
                step='month',
                stepmode='backward'),
            dict(count=1,
                label='1 mo',
                step='month',
                stepmode='backward'),
            dict(step='all')
        ]))

    fig['layout']['xaxis']['rangeselector'] = rangeselector


    # 計算5日移動平均線
    mv_y = df.Close.rolling(5).mean()
    mv_x = list(df.index)

    # Clip the ends
    mv_x = mv_x[5:]
    mv_y = mv_y[5:]

    # 畫上5日移動平均線
    fig['data'].append( dict( x=mv_x, y=mv_y, type='scatter', mode='lines', 
                            line = dict( width = 1 ),
                            marker = dict( color = '#0e51ed' ),
                    yaxis = 'y2', name='5MA' ) )

    # 計算20日移動平均線
    mv_y = df.Close.rolling(20).mean()
    mv_x = list(df.index)
    mv_x = mv_x[20:]
    mv_y = mv_y[20:]

    # 畫上20日移動平均線
    fig['data'].append( dict( x=mv_x, y=mv_y, type='scatter', mode='lines', 
                            line = dict( width = 1 ),
                            marker = dict( color = '#f09307' ),
                    yaxis = 'y2', name='20MA' ) )

    # 計算60日移動平均線
    mv_y = df.Close.rolling(60).mean()
    mv_x = list(df.index)
    mv_x = mv_x[60:]
    mv_y = mv_y[60:]

    # 畫上60日移動平均線
    fig['data'].append( dict( x=mv_x, y=mv_y, type='scatter', mode='lines', 
                            line = dict( width = 1 ),
                            marker = dict( color = '#018a14' ),
                    yaxis = 'y2', name='60MA' ) )


    # 對交易量作圖
    colors = []
    for i in range(len(df.Close)):
        if i != 0:
            if df.Close[i] > df.Close[i-1]:
                colors.append(INCREASING_COLOR)
            else:
                colors.append(DECREASING_COLOR)
        else:
            colors.append(DECREASING_COLOR)

    fig['data'].append( dict( x=df.index, y=df.Volume,                         
                    marker=dict( color=colors ),
                    type='bar', yaxis='y', name='Volume' ) )

    # 計算布林通道
    bb_avg, bb_upper, bb_lower = bbands(df.Close)

    # 畫上布林通道
    fig['data'].append( dict( x=df.index, y=bb_upper, type='scatter', yaxis='y2', 
                            line = dict( width = 1 ),
                            marker=dict(color='#ccc'), hoverinfo='none', 
                            legendgroup='Bollinger Bands', name='Bollinger Bands') )

    fig['data'].append( dict( x=df.index, y=bb_lower, type='scatter', yaxis='y2',
                            line = dict( width = 1 ),
                            marker=dict(color='#ccc'), hoverinfo='none',
                            legendgroup='Bollinger Bands', showlegend=False ) )
    
    # 將畫圖結果輸出
    plot_div = opy.plot(fig, auto_open=False, output_type='div')

    return plot_div



def bbands(price, window_size=10, num_of_std=5):
    rolling_mean = price.rolling(window=window_size).mean()
    rolling_std  = price.rolling(window=window_size).std()
    upper_band = rolling_mean + (rolling_std*num_of_std)
    lower_band = rolling_mean - (rolling_std*num_of_std)
    return rolling_mean, upper_band, lower_band





