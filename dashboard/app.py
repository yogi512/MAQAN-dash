#!/usr/bin/python
from dash import Dash, html, dcc,dash_table
import plotly.express as px
import pandas as pd
from datetime import date
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from scipy.signal import find_peaks
from dash.dependencies import Input, Output
from plotter import plot,parser,table
import dash_bootstrap_components as dbc
import os 
import glob


app = Dash(__name__)
app.title='MAQAN DASHBOARD'


files_list = glob.glob('./data/*.sor') # * means all if need specific format then *.csv
latest_file = max(files_list, key=os.path.getctime)
latest_file_name=latest_file.split('.')[1]
print(latest_file_name)


colors = {
    'background': '#ffffff',
    'text': '#000000'
}

# Dashboard Layout 
df,dff=table(latest_file_name[1:]+'-dump.json')
app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='MAQAN DASHBOARD',
        style={
            'textAlign': 'center',
            'color': colors['text'],
            'font_family':'Montserrat Semibold'
        }
    ),
    # dbc.Container([
    # dbc.Label('Summary'),
    # dash_table.DataTable(df.to_dict('records'),[{"name": i, "id": i} for i in df.columns], id='Table1'),
    # dbc.Alert(id='Table1')
    # ]),
    html.Div([
    dcc.DatePickerSingle(
        id='selectedDate',
        display_format="DD/MM/YYYY",
        min_date_allowed=date(2023,1,1),
        max_date_allowed=date.today(),
        # initial_visible_month=date.today().month,
        date=date.today(),
        style={
        'align':'center'
    },
    ),
   
    html.Div(children='no data for the given date',id='datePicker')
        
    ]),
    # dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns],id='Table1'),
    # dash_table.DataTable(dff.to_dict('records'), [{"name": i, "id": i} for i in df.columns],id='Table2'),
    # dash_table.DataTable(id='Table1',data=df.to_dict('records')), 
    
    dcc.Graph(
        id='Graph1',
        figure=plot(latest_file_name[1:]+'-trace.dat')
    )
    
])



@app.callback(
    Output('datePicker', 'children'),
    Output('Graph1','figure'),
    # Output('Table1','data'),
    # Output('Table2','data'),
    Input('selectedDate', 'date'))

def update_output(date_value):
    if date_value is not None:
        print('Input recieved')
        date_object = date.fromisoformat(date_value)
        date_display = date_object.strftime('%d/%m/%y')
        date_string = date_object.strftime('%d%m%y')
        if('data/'+date_string+'-trace.dat'):
            pass
        else:
            parser(date_string)
        try:
            fig=plot('data/'+date_string+'-trace.dat')
        except:
            fig=plot(latest_file_name[1:]+'-trace.dat')
        
        df,dff=table('data/'+date_string+'-dump.json')

        return date_display,fig
    



if __name__ == '__main__':
    app.run_server(debug=True)