import dash_core_components as dcc
import pandas as pd
import numpy as np
import plotly.graph_objs as go



def get_turbo_detail(df, pathname = None):
    
    timestamp = 1533319533
    # vin = # doesn't matter

    layout = go.Layout(
    title='Turbo',
    yaxis=dict(
        title='Turbine Speed'
    ),
    yaxis2=dict(
        overlaying='y',
        side='right'
    ),
    yaxis3=dict(
        overlaying='y',
        side='right'
    ),
        yaxis4=dict(
        overlaying='y',
        side='right'
    ),
        yaxis5=dict(
        overlaying='y',
        side='right'
    )
    )

    df_critical = df[(df.timestamp_ms > timestamp - 30.0) & (df.timestamp_ms < timestamp + 30.0)]

    trace1=go.Scatter(x=df_critical.datetime, y=df_critical.turbo_turbine_speed,  name = "Turbine Speed")
    trace2=go.Scatter(x=df_critical.datetime, y=df_critical.turbo_waste_gate_position, yaxis='y2', name = "Waste Gate Pos")
    trace3=go.Scatter(x=df_critical.datetime, y=df_critical.turbo_temperature_before_turbine, yaxis='y3', name="Temp. before")
    trace4=go.Scatter(x=df_critical.datetime, y=df_critical.engine_speed, yaxis='y4', name="Engine Speed")

    data=go.Data([trace1, trace2, trace3, trace4])
    figure=go.Figure(data=data,layout=layout)

    return dcc.Graph(
        id='turbodetails1',
        figure={
        'data': data,
        'layout': layout
    })



def get_turbo_detail2(df):

    timestamp = 1533319533

    layout = go.Layout(
    title='Driver Actions',
    yaxis=dict(
        title='Engine Speed'
    ),
    yaxis2=dict(
        overlaying='y',
        side='right'
    ),
    yaxis3=dict(
        overlaying='y',
        side='right'
    ),
        yaxis4=dict(
        overlaying='y',
        side='right'
    ),
        yaxis5=dict(
        overlaying='y',
        side='right'
    )
    )
    df_critical = df[(df.timestamp_ms > timestamp - 30.0) & (df.timestamp_ms < timestamp + 30.0)]

    # trace1=go.Scatter(x=df_critical.datetime, y=df_critical.turbo_turbine_speed, mode = 'markers', name = "Turbine Speed")
    trace2=go.Scatter(x=df_critical.datetime, y=df_critical.engine_speed, name="Engine Spd")
    trace3=go.Scatter(x=df_critical.datetime, y=df_critical.vehicle_speed, yaxis='y3', name="Vehicle Speed")

    trace4=go.Scatter(x=df_critical.datetime, y=df_critical.pedal_position, yaxis='y4', name = "Pedal Position")
    trace5=go.Scatter(x=df_critical.datetime, y=df_critical.gear_engaged, fill='tozeroy',
            opacity=0.01, line=dict(color='rgb(184, 187, 193)'), yaxis='y5', name = "Gear")


    data=go.Data([trace2, trace3, trace4, trace5])
    figure=go.Figure(data=data,layout=layout)

    return dcc.Graph(
            id='turbodetails2',
            figure={
            'data': data,
            'layout': layout
        })