from datetime import datetime as dt
import dash
import dash_html_components as html
import dash_core_components as dcc
import ecu_gadget
import ecu_html_components as eh

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
ecu_temperature_gadget = ecu_gadget.EcuTemperatureGadget()

def get_dashboard_header():
    return html.Div([
        html.H1('Mechanic Panda:  ', style={'color': 'firebrick', 'fontSize': 24, 'display': 'inline'}),
        html.P('Visualizes your engine data.', style={'color': 'firebrick', 'fontSize': 18, 'display': 'inline'})
    ], style= {'width': '40%', 'display': 'block'})

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div([
    get_dashboard_header(),
    html.P(children='ECU Temperature Range'),
    html.Div([
        eh.get_text_field(ecu_temperature_gadget, 'low', 'ECU Temperature (Min)'),
        html.Br(),
        eh.get_text_field(ecu_temperature_gadget, 'high', 'ECU Temperature (Max)'),
    ], style= {'width': '10%', 'display': 'inline-block', 'margin-bottom': '10'}),
    html.Br(),
    html.Button('Filter', id='filter'),
    eh.get_scatter_plot(ecu_temperature_gadget),
    html.Div(id='container'),
    html.Div(dcc.Graph(id='empty', figure={'data': []}), style={'display': 'none'})
])

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
