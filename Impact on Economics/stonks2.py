import numpy as np
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
import streamlit as st

# # Load the data
# Historical data for the dutch stock market is loaded.
AEX = pd.read_csv('AEX.csv')
date_format = '%Y-%m-%d'
AEX.Date = [datetime.strptime(date, date_format) for date in AEX.Date]
AEX['day_diff'] = AEX.Close - AEX.Open
AEX['winloss'] = abs(AEX.day_diff) / AEX.Open

# # Functions
#lets make it more interactive with plotly
def plot_period_stocks(AEX, start_date, end_date, option_list, title):
    """plots the stocks for a given time period"""
    AEX = AEX.loc[AEX['Date'] >= datetime.strptime(start_date, date_format)]
    AEX = AEX.loc[AEX['Date'] <= datetime.strptime(end_date, date_format)]
    traces_list = []

    for option in option_list:
        trace = go.Scatter(x=AEX.Date,
                y=AEX[option],
                name = option,
                )
        traces_list.append(trace)

    Layout = go.Layout(xaxis=dict(showgrid=True, zeroline=True, showticklabels=True),
                       yaxis=dict(showgrid=True, zeroline=True, showticklabels=True),
                       xaxis_title="Date",
                       yaxis_title="Value",
                       title=title,
                        )

    fig = go.Figure(data=traces_list, layout=Layout)
    return fig, AEX

def plot_line_in_fig(fig, AEX_s, date, text, shift=0):
    date_dt = datetime.strptime(date, date_format)
    fig.add_shape(
        # Line Vertical
        dict(
            type="line",
            x0=date_dt,
            y0=(AEX_s.Low).min()+shift,
            x1=date_dt,
            y1=(AEX_s.loc[AEX_s['Date'] == date_dt].Close).values[0],
            line=dict(
                color="Red",
                width=1
            )
    ))
    fig.add_trace(go.Scatter(
        x=[date_dt],
        y=[(AEX_s.Low).min()+shift-15],
        text=[text],
        mode="text",
        showlegend=False,
    ))
    return fig

def plot_shape_in_fig(fig, start_date, end_date, color='green', low=350, high=575):
    from_x = datetime.strptime(start_date, date_format)
    to_x = datetime.strptime(end_date, date_format)
    fig = fig.add_shape(
        # Rectangle reference to the plot
            type="rect",
            xref="x",
            yref="y",
            x0=from_x,
            y0=low,
            x1=to_x,
            y1=high,
            line=dict(
                width=0,
            ),
            fillcolor="green",
            opacity=0.2,
        )
    return fig

st.title('The Effect of COVID-19 on the economy.')
st.write('')

# # General Overview
st.title('General Overview')
option_list = ['Close', 'Open', 'High', 'Low']
title = 'Overview of AEX for past 28 years'
fig, AEX_s = plot_period_stocks(AEX, AEX.Date.min().__format__(date_format), AEX.Date.max().__format__(date_format), option_list, title)
fig = plot_line_in_fig(fig, AEX_s, '1997-07-02', 'Asian crisis',40)
fig = plot_line_in_fig(fig, AEX_s, '1998-08-17', 'Russian Recession')
fig = plot_line_in_fig(fig, AEX_s, '2000-04-14', 'Dotcom', 40)
fig = plot_line_in_fig(fig, AEX_s, '2001-09-10', '9/11', 80)
fig = plot_line_in_fig(fig, AEX_s, '2008-01-02', 'Market Crash 2008')
fig = plot_line_in_fig(fig, AEX_s, '2010-04-27', 'Credit Crisis', 40)
fig = plot_line_in_fig(fig, AEX_s, '2015-06-12', 'China Stock Crash', 40)
fig = plot_line_in_fig(fig, AEX_s, '2018-09-20', 'Stock Market Downturn')
fig = plot_line_in_fig(fig, AEX_s, '2020-02-18', 'Covid-19', 40)
fig

st.write('Looking at these effects, the Dotcom in 2001 and the 2008 market crash had the higest impact on the AEX next to the Covid-19. Because of this we will make an analysis of these crashes (financially forced) and compare them to the Covid-19 situation.')

st.title('Analysis of stock crash')
st.write('We compare the graph for the crash with 2001 and 2008 for the dot.com bubble and the 2008 market crash')

st.markdown('## For the AEX')
st.markdown('Check AEX Stocks from 01-01-2020 till today.')

st.markdown('### For Covid-19')


## options are: 'Close', 'Open', 'High', 'Low', 'day_diff', 'winloss'
option_list = ['Close', 'Open', 'High', 'Low']
title = 'COVID-19'
fig, AEX_s = plot_period_stocks(AEX, '2020-01-01', datetime.today().__format__(date_format), option_list, title)
fig = plot_line_in_fig(fig, AEX_s, '2020-01-24', 'First case EU')
fig = plot_line_in_fig(fig, AEX_s, '2020-02-28', 'First case NL')
fig = plot_shape_in_fig(fig, '2020-01-29', '2020-02-06', high=650)
fig = plot_shape_in_fig(fig, '2020-02-10', '2020-02-24', high=650)
fig = plot_shape_in_fig(fig, '2020-02-28', '2020-03-06', high=650)
fig = plot_shape_in_fig(fig, '2020-03-12', '2020-03-16', high=650)

fig

st.markdown('### For comparisation, stock crash of 2008')
## options are: 'Close', 'Open', 'High', 'Low', 'day_diff', 'winloss'
option_list = ['Close', 'Open', 'High', 'Low']
title = 'The stock market crash in 2008'
fig, AEX_s = plot_period_stocks(AEX, '2007-12-01', '2008-02-18', option_list, title)
fig = plot_line_in_fig(fig, AEX_s, '2008-01-02', 'Market Crash 2008')
fig = plot_shape_in_fig(fig, '2007-12-12', '2007-12-21')
fig = plot_shape_in_fig(fig, '2007-12-22', '2008-01-03')
fig = plot_shape_in_fig(fig, '2008-01-10', '2008-01-15')
fig = plot_shape_in_fig(fig, '2008-01-21', '2008-01-25')
fig

st.markdown('### For comparisation, the dotcom bubble of 2001')
## options are: 'Close', 'Open', 'High', 'Low', 'day_diff', 'winloss'
option_list = ['Close', 'Open', 'High', 'Low']
title = 'The Dotcom bubble 2001 - highest drop in 2001'
fig, AEX_s = plot_period_stocks(AEX, '2001-08-01', '2001-10-15', option_list, title)
fig = plot_line_in_fig(fig, AEX_s, '2001-08-10', 'Dotcom bubble 2001')
fig = plot_shape_in_fig(fig, '2001-08-16', '2001-08-23')
fig = plot_shape_in_fig(fig, '2001-08-24', '2001-08-31')
fig = plot_shape_in_fig(fig, '2001-09-09', '2001-09-14')
fig = plot_shape_in_fig(fig, '2001-09-20', '2001-09-24')
fig


st.markdown('## Re-occurring themes')
st.markdown('All the graphs are of a same time period and show similar trends:')
st.markdown('- There is a period of slight drop in stocks at the beginning')
st.markdown('- Then a small rise in overal stocks')
st.markdown('- then stocks start to drop, but there is an seemfull recovery in the middle')
st.markdown('- then the drop steeply drops to 400 or less.')

st.title('Comparing to other outbreaks')
st.write('First we will have a look at the full market for the AEX, Hang Seng and China Composite for the different epedemic outbreaks.')


option_list = ['Close', 'Open', 'High', 'Low']
title = 'Overview of AEX for past 28 years'
fig, AEX_s = plot_period_stocks(AEX, AEX.Date.min().__format__(date_format), AEX.Date.max().__format__(date_format), option_list, title)
fig = plot_line_in_fig(fig, AEX_s, '1994-09-01', 'Pneumonic Plague')
fig = plot_line_in_fig(fig, AEX_s, '2002-11-18', 'SARS')
fig = plot_line_in_fig(fig, AEX_s, '2006-06-01', 'Avian Flu', 120)
fig = plot_line_in_fig(fig, AEX_s, '2006-09-01', 'Dengue Fever',80)
fig = plot_line_in_fig(fig, AEX_s, '2009-08-03', 'H1N1', 40)
fig = plot_line_in_fig(fig, AEX_s, '2010-11-01', 'Cholera')
fig = plot_line_in_fig(fig, AEX_s, '2013-05-02', 'MERS',80)
fig = plot_line_in_fig(fig, AEX_s, '2014-03-03', 'Ebola', 40)
fig = plot_line_in_fig(fig, AEX_s, '2014-12-03', 'Measles/Rubeola')
fig = plot_line_in_fig(fig, AEX_s, '2016-01-04', 'Zika', 40)
fig = plot_line_in_fig(fig, AEX_s, '2019-06-03', 'Measles', 40)
fig = plot_line_in_fig(fig, AEX_s, '2020-02-18', 'Covid-19')

fig

st.markdown('## Conclusions')
st.markdown('Some Effects rights after certain viral outbreaks can be seen. Look for example at SARS, Avian Flu, H1N1, MERS, Zika. Ofcourse we can not make sound conclusions from this, but the observed effect does seem interesting. To get a better understanding we will zoom in a bit more on SARS and MERS, which were viral outbreaks with large amounts of deaths as well, with SARS beeing maybe the most similar to Covid-19.')

st.title('SARS effect')
st.write('We will look at the three markets, right after the SARS outbreak.')

st.markdown('## For comparisation during the SARS outbreak')
## options are: 'Close', 'Open', 'High', 'Low', 'day_diff', 'winloss'
option_list = ['Close', 'Open', 'High', 'Low']
title = 'AEX during the 2002 /2003 /2004 SARS outbreak (also dotcom bubble)'
fig, AEX_s = plot_period_stocks(AEX, '2002-11-01', '2003-05-01', option_list, title)

# add label and vertical for the sars outbreak date
fig = plot_line_in_fig(fig, AEX_s, '2002-11-18', 'SARS')
fig
