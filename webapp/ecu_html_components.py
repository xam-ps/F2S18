import dash_core_components as dcc

def get_start_date_picker(ecu_temperature_gadget):
    return dcc.DatePickerRange(
        id='start-datetime',
        min_date_allowed=ecu_temperature_gadget.start,
        max_date_allowed=ecu_temperature_gadget.end,
        initial_visible_month=ecu_temperature_gadget.start,
        start_date_placeholder_text='Start',
        end_date=ecu_temperature_gadget.start)

def get_end_date_picker(ecu_temperature_gadget):
    return dcc.DatePickerRange(
        id='end-datetime',
        min_date_allowed=ecu_temperature_gadget.start,
        max_date_allowed=ecu_temperature_gadget.end,
        initial_visible_month=ecu_temperature_gadget.end,
        start_date_placeholder_text='End',
        end_date=ecu_temperature_gadget.end)

def get_range_slider(ecu_temperature_gadget):
    return dcc.RangeSlider(
        id='range-slider',
        marks={i: '{}'.format(i) for i in range(int(ecu_temperature_gadget.low), int(ecu_temperature_gadget.high + 1))},
        min=ecu_temperature_gadget.low,
        max=ecu_temperature_gadget.high,
        step=0.5,
        value=[ecu_temperature_gadget.low, ecu_temperature_gadget.high])
