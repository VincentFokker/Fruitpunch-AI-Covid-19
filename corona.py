import pandas as pd
from matplotlib import pyplot as plt
import random
import streamlit as st

#read the data
daily_cases = pd.read_csv('daily-cases-covid-19-who.csv')
total_cases = pd.read_csv('total-cases-covid-19-who.csv')

#do a split-up
total_cases = total_cases.loc[total_cases['Year'] >= 28]

Total_cases_world = total_cases.loc[total_cases['Entity'] == 'Worldwide']
Total_cases_int = total_cases.loc[total_cases['Entity'] == 'International']
Total_cases_ch = total_cases.loc[total_cases['Entity'] == 'China']

#exclude Worldwide & china from graph
total_cases = total_cases.loc[total_cases['Entity'] != 'Worldwide']
total_cases = total_cases.loc[total_cases['Entity'] != 'International']
total_cases = total_cases.loc[total_cases['Entity'] != 'China']

#add missing data for NL
df2= pd.DataFrame([['Netherlands', 'NLD', 51 , 503], ['Netherlands', 'NLD', 52 , 614]], columns=total_cases.columns)
total_cases = total_cases.append(df2)

country_list = sorted(list(set((total_cases['Entity']))))

import plotly.graph_objects as go
traces_list = []
for item in country_list:
    x = total_cases.loc[total_cases['Entity'] == item]['Year']
#    x = [day - list(total_cases.loc[total_cases['Entity'] == item]['Year'])[0] for day in x]

    trace = go.Scatter(x=x,
            y=total_cases.loc[total_cases['Entity'] == item]['Total confirmed cases of COVID-19'],
            name = item,
            )
    traces_list.append(trace)

Layout = go.Layout(xaxis=dict(showgrid=True, zeroline=True, showticklabels=True),
                   yaxis=dict(showgrid=True, zeroline=True, showticklabels=True),
                   xaxis_title="Days since outbreak",
                   yaxis_title="Amount of infected",
                    )

fig = go.Figure(data=traces_list, layout=Layout)
fig
