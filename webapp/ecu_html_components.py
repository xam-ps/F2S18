import dash_core_components as dcc

def get_date_range_picker(ecu_temperature_gadget):
    return dcc.DatePickerRange(
        id='start-datetime',
        min_date_allowed=ecu_temperature_gadget.start,
        max_date_allowed=ecu_temperature_gadget.end,
        initial_visible_month=ecu_temperature_gadget.start,
        start_date=ecu_temperature_gadget.start,
        end_date=ecu_temperature_gadget.end)

def get_text_field(ecu_temperature_gadget, ele_placeholder, ele_id):
    return dcc.Input(
        id = ele_id,
        placeholder=ele_placeholder,
        type='text',
        value='')

def get_scatter_plot(ecu_temperature_gadget, convert=False):
    return dcc.Graph(
        id='ecu_temperature_scatter_plot',
        figure={
            'data': [
                {'x': ecu_temperature_gadget.df_agg_740.timestamp,
                'y': ecu_temperature_gadget.df_agg_740.ECU_Temperature,
                'type': 'scatter', 'name': 'ECU_Temperature',
                'mode' : 'markers'}
            ],
            'layout': {
                'title': 'ECU_Temperature vs Time'
            }
        },
        style={'width': '1300', 'height' : '1200'}
    )
