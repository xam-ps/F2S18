import dash_core_components as dcc

def get_text_field(ecu_temperature_gadget, ele_id, ele_placeholder):
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
