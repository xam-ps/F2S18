# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import flask
import os

# ECU Gadget imports begin
import ecu_gadget as ec
import ecu_html_components as ehc

# Turbo related
import turbo

# load on start
df = pd.read_csv("data/turbo_small.csv")
df['datetime'] = pd.to_datetime(df.datetime)


# ECU Gadget imports end
external_stylesheets = ['static/style.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
ecu_temperature_gadget = ec.EcuTemperatureGadget()

STATIC_PATH = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'static')


@app.server.route('/static/<resource>')
def serve_static(resource):
    return flask.send_from_directory(STATIC_PATH, resource)


app.layout = html.Div(children=[
    html.Meta(name='viewport', content='width=device-width, initial-scale=1.0'),
    html.Link(rel='shortcut icon', href='static/favicon.ico'),

    html.Div([
        html.Img(src='static/mechPandaProfile.png',
                 height='40', width='40', className='accountPic'),
        html.P('Mechanic Panda', className='accountName')
    ], className="account"),

    html.Div([
        html.Div([
            html.P('Time Range'),
            dcc.RangeSlider(
                count=1,
                min=-60,
                max=0,
                step=1.0,
                marks={
                    -60: '-60 Days',
                    -40: '-40 Days',
                    -20: '-20 Days',
                    0: 'today'
                },
                value=[-5, 0]
            )], className='slider'),
        html.Div(
            dcc.Input(
                placeholder='Search (VIN, Brand, etc.)',
                type='text',
                value=''
            ), className='search'),
    ], className='header'),

    html.Div([
        html.Div([
            html.Div(
                #need to pass the start and end from the slider callback
                ehc.get_pie_chart(ecu_temperature_gadget),
                className='test'),
        ], className='charts'),
        html.Div([
            html.Div(
                # Replace this one for the upper sidebar widget
                turbo.get_turbo_alerts(df),
                className='upper'),
            html.Div(
                # Replace this one for the lower sidebar widget
                ehc.get_alert_table(ecu_temperature_gadget),
                className='lower'),
        ], className='sidebar'),
    ], className='main'),

])

if __name__ == '__main__':
    app.run_server(debug=True)
