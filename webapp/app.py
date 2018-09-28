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
df = pd.read_csv("data/turbo.csv")
df['datetime'] = pd.to_datetime(df.datetime)


# ECU Gadget imports end
external_stylesheets = ['static/style.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

ecu_temperature_gadget = ec.EcuTemperatureGadget()

STATIC_PATH = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'static')


@app.server.route('/static/<resource>')
def serve_static(resource):
    return flask.send_from_directory(STATIC_PATH, resource)

index_page = html.Div(children=[
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
            dcc.Link(
                html.Div(
                #need to pass the start and end from the slider callback
                ehc.get_pie_chart(ecu_temperature_gadget),
                className='test')
                , href='/ecu'),
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

turbo = html.Div([
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

    html.Div([html.P('Turbo drilldown'),
        # Put in Turbo drilldown code here
    ], className='main'),
])

ecu = html.Div([
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

    html.Div([html.P('ECU History View'),
        # Put in ECU drilldown code here
        html.P(children='ECU Temperature Range'),
        html.Div([
            ehc.get_text_field(ecu_temperature_gadget, 'low', 'ECU Temperature (Min)'),
            html.Br(),
            ehc.get_text_field(ecu_temperature_gadget, 'high', 'ECU Temperature (Max)'),
        ], style= {'width': '10%', 'display': 'inline-block', 'margin-bottom': '10'}),
        html.Br(),
        html.Button('Filter', id='filter'),
        ehc.get_scatter_plot(ecu_temperature_gadget),
        html.Div(id='container'),
        html.Div(dcc.Graph(id='empty', figure={'data': []}), style={'display': 'none'})
    ], className='main'),
])

@app.callback(dash.dependencies.Output('page-content', 'children'),
    [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/ecu':
        return ecu
    elif pathname == '/turbo':
        return turbo
    else:
        return index_page

@app.callback(
    dash.dependencies.Output('container', 'children'),
    [dash.dependencies.Input('low', 'value'),
     dash.dependencies.Input('high', 'value')])
def update_output(low, high):
    if low == '' or high == '':
        return
    df_out, df_norm = ecu_temperature_gadget.filter_data(int(low), int(high))
    graph = dcc.Graph(
            id='barviz',
            figure={
                'data': [{
                    'x': ['Median Vehicle Speed', 'Median Engine Speed', 'Avg. Fuel_Pressure', 'Avg. Engine_Inlet_Temperture'],
                    'y': [df_out['Vehicle_Speed'].median(), df_out['Engine_Speed'].median(),
                            df_out['Fuel_Pressure'].mean(), df_out['Engine_Inlet_Temperture'].mean()],
                    'type': 'bar', 'name' : 'Outlier ECU Temperature'
                    },
                    {
                        'x': ['Median Vehicle Speed', 'Median Engine Speed', 'Avg. Fuel_Pressure', 'Avg. Engine_Inlet_Temperture'],
                        'y': [df_norm['Vehicle_Speed'].median(), df_norm['Engine_Speed'].median(),
                                df_norm['Fuel_Pressure'].mean(), df_norm['Engine_Inlet_Temperture'].mean()],
                        'type': 'bar', 'name' : 'Normal ECU Temperature'
                    }
                ],
                'layout': {
                    'title': 'Outlier Parameters vs Normal Parameters',
                    'barmode': 'group'
                }
            }
        )
    return html.Div(graph)

if __name__ == '__main__':
    app.run_server(debug=True)
