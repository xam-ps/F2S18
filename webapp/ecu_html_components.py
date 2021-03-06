import dash_core_components as dcc

def get_text_field(ecu_temperature_gadget, ele_id, ele_placeholder):
    return dcc.Input(
        id = ele_id,
        placeholder=ele_placeholder,
        type='text',
        value='',
        style={'margin-left': '5'})

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

def get_pie_chart(ecu_temperature_gadget, start = None, end = None):
    if not start or not end:
        start = ecu_temperature_gadget.start
        end = ecu_temperature_gadget.end

    above_normal, normal = ecu_temperature_gadget.get_vehicle_percentage_above_normal_for_time_window(start, end)
    return dcc.Graph(
        id = "ECU_Pie",
        figure = {
            'data' : [
                {
                    'labels': ['Abnormal ECU Temp.', 'Normal ECU Temp.'],
                    'values': [above_normal, normal],
                    'type': 'pie'
                }
            ],
            'layout': {
                'title': 'Fleet ECU Temperature Monitor',
                'legend': dict(orientation="h")
            }
        }
    )

def get_alert_table(ecu_temperature_gadget, start = None, end = None):
    if not start or not end:
        start = ecu_temperature_gadget.start
        end = ecu_temperature_gadget.end

    df = ecu_temperature_gadget.get_vehicle_details_above_normal_for_time_window(start, end)
    df = df.sort_values('ECU_Temperature', ascending = False)
    return dcc.Graph(
        id = "ECU_Alert",
        figure = {
            'data': [
                {
                    'header': dict(values=df.columns, fill = dict( color = 'rgb(238,238,238)' )),
                    'cells': dict(values=[df.timestamp, df.ECU_Temperature, df.Vehicle_Number]),
                    'type': 'table'
                }
            ],
        },
        style={'width': '700', 'height' : '400'}
    )

def get_hist(ecu_temperature_gadget):
    print('get_hist called')
    df_out, df_norm = ecu_temperature_gadget.filter_data(90, 100)
    return dcc.Graph(
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
