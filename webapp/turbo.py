import dash_core_components as dcc
import pandas as pd
import numpy as np


#df = pd.read_csv("turbo.csv")
#df['datetime'] = pd.to_datetime(df.datetime)

def get_turbo_alerts(df):
    df_grouped_turbine_speed = df.groupby([df.vehicle_number, df.datetime.dt.year, df.datetime.dt.month, df.datetime.dt.day, df.datetime.dt.hour, df.datetime.dt.minute]).agg({'turbo_turbine_speed':'max'})
    critical_turbine_speeds = df_grouped_turbine_speed[df_grouped_turbine_speed.turbo_turbine_speed > 235000].turbo_turbine_speed.unique()
    critical_turbine_speeds = [str(x) for x in critical_turbine_speeds]
    
    df = df[df.turbo_turbine_speed.astype(str).isin(critical_turbine_speeds)]
    df.turbo_turbine_speed = round(df.turbo_turbine_speed)
    

    graph = dcc.Graph(
        id = "alert-table",
        figure = {
            'data': [
                {
                'header': dict(values=['Time', 'VIN', 'Turbine Speed'],fill = dict(color='#C2D4FF'),
                align = ['left'] * 5),
                'cells': dict(values=[df.datetime, df.vehicle_number, df.turbo_turbine_speed]),
                'type': 'table'
                }
            ]
        }
    )


    return graph
    


def get_turbo_detail(df):

    return None




