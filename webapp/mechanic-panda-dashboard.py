from datetime import datetime as dt
import dash
import dash_html_components as html
import dash_core_components as dcc
import ecu_gadget

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

def get_dashboard_header():
    return html.H1(children='Mechanic Panda')

def get_dashboard_description():
    return html.Div(children='''
        Visualizes your engine data.
    ''')

ecu_temperature_gadget = ecu_gadget.EcuTemperatureGadget()
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div([
    get_dashboard_header(),
    get_dashboard_description(),
    dcc.DatePickerRange(
        id='start-datetime',
        min_date_allowed=ecu_temperature_gadget.start,
        max_date_allowed=ecu_temperature_gadget.end,
        initial_visible_month=ecu_temperature_gadget.start,
        end_date=ecu_temperature_gadget.end
    ),
    html.Div(id='output-container-start-date-picker-range'),
    dcc.DatePickerRange(
        id='end-datetime',
        min_date_allowed=ecu_temperature_gadget.start,
        max_date_allowed=ecu_temperature_gadget.end,
        initial_visible_month=ecu_temperature_gadget.end,
        end_date=ecu_temperature_gadget.end
    ),
    html.Div(id='output-container-end-date-picker-range')
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
