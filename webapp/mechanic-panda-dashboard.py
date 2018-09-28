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
    html.Div([
        eh.get_start_date_picker(ecu_temperature_gadget),
        eh.get_end_date_picker(ecu_temperature_gadget)
    ], style= {'width': '40%', 'display': 'inline-block'}),
    html.H3(children='ECU_Temperature Range'),
    eh.get_range_slider(ecu_temperature_gadget),
    html.Div(id='output-container-range-slider')
])

'''
@app.callback(
    dash.dependencies.Output('output-container-date-picker-range', 'children'),
    [dash.dependencies.Input('start-datetime', 'start_date'),
     dash.dependencies.Input('end-datetime', 'end_date')])
def update_output(start_date, end_date):
    string_prefix = 'You have selected: '
    if start_date is not None:
        start_date = dt.strptime(start_date, '%Y-%m-%d')
        start_date_string = start_date.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'Start Date: ' + start_date_string + ' | '
    if end_date is not None:
        end_date = dt.strptime(end_date, '%Y-%m-%d')
        end_date_string = end_date.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'End Date: ' + end_date_string
    if len(string_prefix) == len('You have selected: '):
        return 'Select a date to see it displayed here'
    else:
        return string_prefix
'''

if __name__ == '__main__':
    app.run_server(debug=True)
