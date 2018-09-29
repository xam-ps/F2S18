# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import State
import pandas as pd
import flask
import os
import distance

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
for css in external_stylesheets:
    app.css.append_css({"external_url": css})
app.scripts.append_script(
    {"external_url": "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"})
app.scripts.append_script(
    {"external_url": "https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"})
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
        dcc.Link(html.Img(src='static/mechPandaProfile.png',
                          height='40', width='40', className='accountPic'), href='/'),
        html.P('Mechanic Panda', className='accountName'),
        html.Img(src='static/user.png',
                 height='40', width='40', className='userPic'),
        html.P('Adam Smith', className='userName'),
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
            html.Div([
                html.Div('Vehicles in Maintenance:'),
                html.Div('5', className='mainNumber')
            ], className='maintenance smallBox'),
            dcc.Link(
                html.Div([
                    html.Div('Ø KM per car and day:'),
                    html.Div('155,4', className='mainNumber')
                ], className='km maintenance smallBox'), href='/km'),
            html.Div([
                html.Div('Ø fuel consumption (l/100km):'),
                html.Div('8,7', className='mainNumber')
            ], className='maintenance smallBox'),
            html.Div([
                html.Div('Max KM per Day:'),
                html.Div('965', className='mainNumber'),
                html.Div('27.09.2018', className='smallNumber')
            ], className='maintenance smallBox'),
            dcc.Link(
                html.Div(
                    # need to pass the start and end from the slider callback
                    ehc.get_pie_chart(ecu_temperature_gadget),
                    className='test'), href='/ecu'),
        ], className='charts'),
        html.Div([
            html.P('Alerts (5):', className='alertsHeading'),
            html.Div([
                dcc.Link(
                    html.Div([
                        html.Small("Vehicle: VF1RFA00958456258")
                    ], className="alert alert-danger"), href='/turbo'),
                dcc.Link(
                    html.Div([
                        html.Small("Vehicle: VF1RFA00851236548")
                    ], className="alert alert-danger"),
                    href='/turbo'),
                dcc.Link(
                    html.Div([
                        html.Small("Vehicle: VF1RFA00951485624")
                    ], className="alert alert-danger"),
                    href='/turbo'),
                html.Div([
                    html.Small("Vehicle: VF1RFA00357138740")
                ], className="alert alert-danger"),
                html.Div([
                    html.Small("Vehicle: VF1RFA00357138714")
                ], className="alert alert-danger"),
            ], className="row"),
            html.P('Notifications (1):', className='alertsHeading notifications'),
            html.Div([
                html.Div([
                    html.Small("Vehicle: VF1RFA00841247845")
                ], className="alert alert-warning"),
            ], className="row"),
        ], className='sidebar'),
    ], className='main'),

])

turbo = html.Div([
    html.Meta(name='viewport', content='width=device-width, initial-scale=1.0'),
    html.Link(rel='shortcut icon', href='static/favicon.ico'),

    html.Div([
        dcc.Link(html.Img(src='static/mechPandaProfile.png',
                          height='40', width='40', className='accountPic'), href='/'),
        html.P('Mechanic Panda', className='accountName'),
        html.Img(src='static/user.png',
                 height='40', width='40', className='userPic'),
        html.P('Adam Smith', className='userName'),
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

    html.Div([html.P('Turbo drilldown', className='turboHeading'),
              html.Div(turbo.get_turbo_detail(df), className='detail1'),
              html.Div(turbo.get_turbo_detail2(df), className='details2')
              ], className='main'),
])

km = html.Div([
    html.Meta(name='viewport', content='width=device-width, initial-scale=1.0'),
    html.Link(rel='shortcut icon', href='static/favicon.ico'),

    html.Div([
        dcc.Link(html.Img(src='static/mechPandaProfile.png',
                          height='40', width='40', className='accountPic'), href='/'),
        html.P('Mechanic Panda', className='accountName'),
        html.Img(src='static/user.png',
                 height='40', width='40', className='userPic'),
        html.P('Adam Smith', className='userName'),
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

    html.Div([html.P('Average distance per day', className='turboHeading'),
              html.Div(distance.get_avg_distance_chart())
              ]),
])

ecu = html.Div([
    html.Meta(name='viewport', content='width=device-width, initial-scale=1.0'),
    html.Link(rel='shortcut icon', href='static/favicon.ico'),

    html.Div([
        dcc.Link(html.Img(src='static/mechPandaProfile.png',
                          height='40', width='40', className='accountPic'), href='/'),
        html.P('Mechanic Panda', className='accountName'),
        html.Img(src='static/user.png',
                 height='40', width='40', className='userPic'),
        html.P('Adam Smith', className='userName'),
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

    html.Div([html.P('ECU History View', className='turboHeading'),
              # Put in ECU drilldown code here
              html.Div([
                  ehc.get_text_field(ecu_temperature_gadget,
                                     'low', 'ECU Temp. (Min)'),
                  ehc.get_text_field(ecu_temperature_gadget,
                                     'high', 'ECU Temp. (Max)')
              ], style={'margin': '9', 'display': 'inline'}),
              dcc.Link(
        html.Button('Filter', id='filter', style={'color': 'white', 'background-color': 'steelblue', 'height': '30', 'width': '70', 'margin': '9'}), href='/ecu_hist'
    ),
        ehc.get_scatter_plot(ecu_temperature_gadget)
    ], className='main'),
])


def get_ecu_hist():
    ecu_hist = html.Div([
        html.Meta(name='viewport',
                  content='width=device-width, initial-scale=1.0'),
        html.Link(rel='shortcut icon', href='static/favicon.ico'),

        html.Div([
            dcc.Link(html.Img(src='static/mechPandaProfile.png',
                              height='40', width='40', className='accountPic'), href='/'),
            html.P('Mechanic Panda', className='accountName'),
            html.Img(src='static/user.png',
                     height='40', width='40', className='userPic'),
            html.P('Adam Smith', className='userName'),
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
        ehc.get_hist(ecu_temperature_gadget)
    ])
    return ecu_hist


@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if '/ecu_hist' in str(pathname):
        return get_ecu_hist()
    elif '/ecu' in str(pathname):
        return ecu
    elif '/km' in str(pathname):
        return km
    elif '/turbo' in str(pathname):
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
                'type': 'bar', 'name': 'Outlier ECU Temperature'
            },
                {
                'x': ['Median Vehicle Speed', 'Median Engine Speed', 'Avg. Fuel_Pressure', 'Avg. Engine_Inlet_Temperture'],
                'y': [df_norm['Vehicle_Speed'].median(), df_norm['Engine_Speed'].median(),
                      df_norm['Fuel_Pressure'].mean(), df_norm['Engine_Inlet_Temperture'].mean()],
                'type': 'bar', 'name': 'Normal ECU Temperature'
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
