from datetime import datetime as dt
import dash
import dash_html_components as html
import dash_core_components as dcc
import ecu_gadget
import ecu_html_components as eh
from app import app



ecu_temperature_gadget = ecu_gadget.EcuTemperatureGadget()

page_layout_ecu = html.Div([
    dcc.Link('Home', href='/'),
    html.Form([
        html.Div([
            html.P(children='ECU Temperature Range'),
            eh.get_text_field(ecu_temperature_gadget, 'low', 'ECU Temperature (Min)'),
            eh.get_text_field(ecu_temperature_gadget, 'high', 'ECU Temperature (Max)')
        ], className="form-group"),
        html.Button('Filter', id='filter')
    ], className="form-inline"),
    eh.get_scatter_plot(ecu_temperature_gadget),
    html.Div(id='container'),
    html.Div(dcc.Graph(id='empty', figure={'data': []}), style={'display': 'none'})
])
'''
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
'''
