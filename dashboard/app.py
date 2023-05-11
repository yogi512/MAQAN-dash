#!/usr/bin/python
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
from datetime import date
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from scipy.signal import find_peaks
from dash.dependencies import Input, Output

app = Dash(__name__)

df1= pd.read_table('data/RP_1_0001-trace.dat', sep='\s+')
df1.columns=['Distance','dB']
indices = find_peaks(df1['dB'],height=20)[0]
print(indices)


# Plotting the dataframe
fig = go.Figure()
fig.add_trace(go.Line(
    x=df1['Distance'],
    y=df1['dB'],   
    name='Loss'
   
    # mode='lines+markers',
))

# Plotting the Peaks
names=['ERNET','SETS','']
fig.add_trace(go.Scatter(
    x=[df1['Distance'][i] for i in indices if i!=''],
    y=[df1['dB'][j] for j in indices if j!=''],
    text=['ERNET','SETS','GHOST'],
    textposition="top center",
    mode='markers+text',
    marker=dict(
        size=8,
        color='red',
        symbol='cross'
    ),
    name='Peaks'
))

# Updating Style
fig.update_layout(
    title={'text':"OTDR Trace ",'font_size':34},
    xaxis_title="Distance (km)",
    yaxis_title="dB",
    font_family="Montserrat Semibold",
    font_color="black"   
)
fig.update_traces(line_color='#1c1480')
colors = {
    'background': '#ffffff',
    'text': '#000000'
}

# Dashboard Layout 
app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='MAQAN DASHBOARD',
        style={
            'textAlign': 'center',
            'color': colors['text'],
            'font_family':'Montserrat Semibold'
        }
    ),
    html.Div([
    dcc.DatePickerSingle(
        id='selectedDate',
        display_format="DD MM YYYY",
        min_date_allowed=date(2023,1,1),
        max_date_allowed=date.today(),
        initial_visible_month=date.today().month,
        date=date.today(),
        style={
        'align':'center'
    },
    ),
    html.Div(id='datePicker')
    
    ]),
    dcc.Graph(
        id='Graph1',
        figure=fig
    )
    
])


@app.callback(
    Output('datePicker', 'children'),
    Input('selectedDate', 'date'))
def update_output(date_value):
    string_prefix = 'You have selected: '
    if date_value is not None:
        date_object = date.fromisoformat(date_value)
        date_string = date_object.strftime('%d %B %Y')
        return string_prefix + date_string

if __name__ == '__main__':
    app.run_server(debug=False)