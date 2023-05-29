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
    'text': '#ffffff'
}

# Dashboard Layout 
df,dff=table(latest_file_name[1:]+'-dump.json')
app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.Div(style={'backgroundColor': '#1d1480','color': colors['text'],'height':'150px'},
    children=[
    html.H1(children='METROPOLITAN QUANTUM ACCESS NETWORK'),
    html.H2('OTDR Dashboard',style={'color': colors['text'],'textAlign': 'center','font_family':'Montserrat'})
    ]),
    
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
    
    html.H2(children='\nSummary'),
    dash_table.DataTable(id='Table2',data=dff.to_dict('records')), 
    html.H2(children='Trace Data'),         
    dash_table.DataTable(id='Table1',data=df.to_dict('records')),
    html.H2(children='Trace Plot'),
    
    dcc.Graph(
        id='Graph1',
        figure=plot(latest_file_name[1:]+'-trace.dat')
    )
    
])



@app.callback(
    Output('datePicker', 'children'),
    Output('Graph1','figure'),
    Output('Table1','data'),
    Output('Table2','data'),
    Input('selectedDate', 'date'))

def update_output(date_value):
    if date_value is not None:
        print('Input recieved')
        date_object = date.fromisoformat(date_value)
        date_display = date_object.strftime('%d/%m/%y')
        date_out='The data for the date '+date_display+' is displayed below'
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

        return date_out,fig,df.to_dict('records'),dff.to_dict('records')
    



if __name__ == '__main__':
    app.run_server(debug=True)