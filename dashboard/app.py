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
from plotter import plot,parser

app = Dash(__name__)


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
        # initial_visible_month=date.today().month,
        date=date.today(),
        style={
        'align':'center'
    },
    ),
    # html.Div(id='datePicker')
    
    ]),
    dcc.Graph(
        id='Graph1',
        figure=plot('data/110523-trace.dat')
    )
    
])


@app.callback(
    # Output('datePicker', 'children'),
    Output('Graph1','figure'),
    Input('selectedDate', 'date'))
def update_output(date_value):
    if date_value is not None:
        date_object = date.fromisoformat(date_value)
        date_string = date_object.strftime('%d%m%y')
        if('data/'+date_string+'-trace.sor'):
            pass
        parser(date_string)
        fig=plot('data/'+date_string+'-trace.dat')
        
        return fig
    



if __name__ == '__main__':
    app.run_server(debug=True)