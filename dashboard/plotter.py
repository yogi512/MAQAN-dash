import plotly.express as px
import pandas as pd
from datetime import date
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from scipy.signal import find_peaks
import os
import json



def parser(date_string):
    os.chdir('./data')
    filename= date_string+'.sor'
    os.system('pyOTDR {}'.format(filename))
    os.chdir('..')

def table(filename):
    f = open(filename)
    data = json.load(f)
    l=[]
    for i in range(1,100):
        try:
            l.append((data['KeyEvents']['event {}'.format(i)]['distance'],
                    data['KeyEvents']['event {}'.format(i)]['refl loss'],
                    data['KeyEvents']['event {}'.format(i)]['splice loss'],
                    data['KeyEvents']['event {}'.format(i)]['peak'],
                    data['KeyEvents']['event {}'.format(i)]['end of curr'],
                    data['KeyEvents']['event {}'.format(i)]['end of prev'],
                    data['KeyEvents']['event {}'.format(i)]['slope'],
                    data['KeyEvents']['event {}'.format(i)]['start of curr'],
                    data['KeyEvents']['event {}'.format(i)]['start of next'],
                    data['KeyEvents']['event {}'.format(i)]['type']))
        except:
            break
    df = pd.DataFrame(l, columns =['Distance','ReflectionLoss','SpliceLoss','Peak','EndOfCurr','EndOfPrev','Slope','StartOfCurr','StartOfNext','Type'])
    df = df.drop(['EndOfCurr','EndOfPrev','StartOfCurr','StartOfNext','Peak','Slope','Type'],axis=1)
    
    out={'Date/time':data['FxdParams']['date/time'][0:19],
     'Wavelength':data['FxdParams']['wavelength'],
     'Pulse width':data['FxdParams']['pulse width'],
     'Range':data['FxdParams']['range'],
     'Resolution':data['FxdParams']['resolution']}
    
    dff = pd.DataFrame.from_dict(out,orient='index',columns=['Value'])
    return df,dff

def plot(filename):
    df1= pd.read_table(filename, sep='\s+')
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
        # title={'text':"OTDR Trace ",'font_size':24},
        xaxis_title="Distance (km)",
        yaxis_title="dB",
        font_family="Montserrat Semibold",
        font_color="black"   
    )
    fig.update_traces(line_color='#1c1480')
    return fig
