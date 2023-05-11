import plotly.express as px
import pandas as pd
from datetime import date
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from scipy.signal import find_peaks

def plot():
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
        title={'text':"OTDR Trace ",'font_size':24},
        xaxis_title="Distance (km)",
        yaxis_title="dB",
        font_family="Montserrat Semibold",
        font_color="black"   
    )
    fig.update_traces(line_color='#1c1480')
    return fig
