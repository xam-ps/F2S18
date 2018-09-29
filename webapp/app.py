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
external_stylesheets = ['static/style.css', "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css",
                    "https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
for css in external_stylesheets:
    app.css.append_css({"external_url": css})
app.scripts.append_script({"external_url": "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"})
app.scripts.append_script({"external_url": "https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"})
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
            #Add the relevant data here
            html.Div([
                html.Div([
                    html.Small("Turbine Speed: 235925.0 ", style={'display' : 'inline-block'}),
                    html.Small("Timestamp: 2018-08-01 17:29:43 ", style={'display' : 'inline-block'}),
                    html.Small("Vehicle: VF1RFA00357138740", style={'display' : 'inline-block'})
                ], className="alert alert-danger", style={'width': '70%'}),
                html.Div([
                    html.Small("Turbine Speed: 238318.0  ", style={'display' : 'inline-block'}),
                    html.Small("Timestamp: 2018-08-01 17:29:43 ", style={'display' : 'inline-block'}),
                    html.Small("Vehicle: VF1RFA00357138740", style={'display' : 'inline-block'})
                ], className="alert alert-danger", style={'width': '70%'}),
                html.Div([
                    html.Small("Turbine Speed: 242303.0  ", style={'display' : 'inline-block'}),
                    html.Small("Timestamp: 2018-08-01 17:29:43 ", style={'display' : 'inline-block'}),
                    html.Small("Vehicle: VF1RFA00357138740", style={'display' : 'inline-block'})
                ], className="alert alert-danger", style={'width': '70%'})
            ], className="row"),
            html.Div([
                html.Div([
                    html.Small("ECU Temperature: 180 C ", style={'display' : 'inline-block'}),
                    html.Small("Timestamp: 2018-08-01 17:29:43 ", style={'display' : 'inline-block'}),
                    html.Small("Vehicle: VF1RFA00357138740", style={'display' : 'inline-block'})
                ], className="alert alert-danger", style={'width': '70%'}),
                html.Div([
                    html.Small("ECU Temperature: 150 C ", style={'display' : 'inline-block'}),
                    html.Small("Timestamp: 2018-08-03 12:19:33 ", style={'display' : 'inline-block'}),
                    html.Small("Vehicle: VF1RFA00357138740", style={'display' : 'inline-block'})
                ], className="alert alert-warning", style={'width': '70%'}),
                html.Div([
                    html.Small("ECU Temperature: 170 C ", style={'display' : 'inline-block'}),
                    html.Small("Timestamp: 2018-08-04 11:09:36 ", style={'display' : 'inline-block'}),
                    html.Small("Vehicle: VF1RFA00357138714", style={'display' : 'inline-block'})
                ], className="alert alert-danger", style={'width': '70%'})
            ], className="row"),
        ], className='col-12 col-md-4', style={'display':'inline-block'}),
        html.Div([
            html.Div([
                dcc.Link(
                    html.Div([
                    #need to pass the start and end from the slider callback
                    ehc.get_pie_chart(ecu_temperature_gadget)], style={'display':'inline'})
                    , href='/ecu'
                )
            ], style={'display':'inline'}),
            html.Div([
                ehc.get_pie_chart(ecu_temperature_gadget)
            ], style={'display':'inline'})
        ], className = "col-12 col-md-8", style={"display":"inline"})
    ], className="main"),

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

    html.Div([html.P('Turbo drilldown'),
                html.Div(turbo.get_turbo_detail(df), className='detail1'),
                html.Div(turbo.get_turbo_detail2(df), className='details2')
              ], className='main'),
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

    html.Div([html.P('ECU History View'),
        # Put in ECU drilldown code here
        html.Form([
            html.Div([
                ehc.get_text_field(ecu_temperature_gadget, 'low', 'ECU Temp. (Min)'),
                ehc.get_text_field(ecu_temperature_gadget, 'high', 'ECU Temp. (Max)')
            ], className="form-group"),
            dcc.Link(
                html.Button('Filter', id='filter', style={'margin-left': '5'}, className="btn btn-info btn-lg")
                , href='/ecu_hist'
            )
        ], className="form-inline"),
        ehc.get_scatter_plot(ecu_temperature_gadget),
    ], className='main'),
])

ecu_hist = html.Div([
    ehc.get_hist(ecu_temperature_gadget)
])

@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if '/ecu' in str(pathname):
        return ecu
    elif '/turbo' in str(pathname):
        return turbo
    elif pathname == '/ecu_hist':
        return ecu_hist
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
