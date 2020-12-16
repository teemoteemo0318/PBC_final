import plotly.graph_objects as go
import plotly.offline as opy
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
# import plotly.graph_objs as go 


# https://chart-studio.plotly.com/~jackp/17421/plotly-candlestick-chart-in-python/#/
def historical_pic(df):
    INCREASING_COLOR = '#cf1717'
    DECREASING_COLOR = '#138f36'
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

    fig = dict( data=data, layout=layout )
    fig['layout'] = dict()
    fig['layout']['hovermode'] = "x unified"
    fig['layout']['plot_bgcolor'] = 'rgb(250, 250, 250)'
    fig['layout']['height'] = 600
    fig['layout']['width'] = 1200
    fig['layout']['xaxis'] = dict( rangeselector = dict( visible = True ) )
    fig['layout']['yaxis'] = dict( domain = [0, 0.2], showticklabels = False, fixedrange = False)
    fig['layout']['yaxis2'] = dict( domain = [0.2, 0.8])
    fig['layout']['legend'] = dict( orientation = 'h', y=0.9, x=0.3, yanchor='bottom' )
    fig['layout']['margin'] = dict( t=40, b=40, r=40, l=40 )

# https://plotly.com/python/range-slider/
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



    mv_y = movingaverage(df.Close,5)
    mv_x = list(df.index)

    # Clip the ends
    mv_x = mv_x[5:-5]
    mv_y = mv_y[5:-5]

    fig['data'].append( dict( x=mv_x, y=mv_y, type='scatter', mode='lines', 
                            line = dict( width = 1 ),
                            marker = dict( color = '#0e51ed' ),
                    yaxis = 'y2', name='5MA' ) )

    mv_y = movingaverage(df.Close,20)
    mv_x = list(df.index)
    mv_x = mv_x[10:-10]
    mv_y = mv_y[10:-10]

    fig['data'].append( dict( x=mv_x, y=mv_y, type='scatter', mode='lines', 
                            line = dict( width = 1 ),
                            marker = dict( color = '#f09307' ),
                    yaxis = 'y2', name='20MA' ) )

    mv_y = movingaverage(df.Close,60)
    mv_x = list(df.index)
    mv_x = mv_x[30:-30]
    mv_y = mv_y[30:-30]

    fig['data'].append( dict( x=mv_x, y=mv_y, type='scatter', mode='lines', 
                            line = dict( width = 1 ),
                            marker = dict( color = '#018a14' ),
                    yaxis = 'y2', name='60MA' ) )


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

    # bb_avg, bb_upper, bb_lower = bbands(df.Close)

    # fig['data'].append( dict( x=df.index, y=bb_upper, type='scatter', yaxis='y2', 
    #                         line = dict( width = 1 ),
    #                         marker=dict(color='#ccc'), hoverinfo='none', 
    #                         legendgroup='Bollinger Bands', name='Bollinger Bands') )

    # fig['data'].append( dict( x=df.index, y=bb_lower, type='scatter', yaxis='y2',
    #                         line = dict( width = 1 ),
    #                         marker=dict(color='#ccc'), hoverinfo='none',
    #                         legendgroup='Bollinger Bands', showlegend=False ) )
    plot_div = opy.plot(fig, auto_open=False, output_type='div')

    return plot_div

def movingaverage(interval, window_size=10):
    window = np.ones(int(window_size))/float(window_size)
    return np.convolve(interval, window, 'same')


def bbands(price, window_size=10, num_of_std=5):
    rolling_mean = price.rolling(window=window_size).mean()
    rolling_std  = price.rolling(window=window_size).std()
    upper_band = rolling_mean + (rolling_std*num_of_std)
    lower_band = rolling_mean - (rolling_std*num_of_std)
    return rolling_mean, upper_band, lower_band


