import os
import pandas as pd

class EcuTemperatureGadget():

    def __init__(self):
        self.df_agg_740 = self.load_aggregated_data_740()
        print(f'Shape of loaded data: {self.df_agg_740.shape}')
        self.convert_timestamp()
        self.reset_index()
        self.start = min(self.df_agg_740['timestamp'])
        self.end = max(self.df_agg_740['timestamp'])
        self.low = min(self.df_agg_740['ECU_Temperature'])
        self.high = max(self.df_agg_740['ECU_Temperature'])
        print(f'Timestamp range: {self.start} - {self.end}')
        print(f'ECU_Temperature range: {self.low} - {self.high}')

    def load_aggregated_data_740(self):
        files = [f'data{os.sep}{d}' for d in os.listdir('data') if '.csv' in d]
        print(f'Loading Aggregated file: {files[0]}')
        return pd.read_csv(files[0])

    def convert_timestamp(self):
        self.df_agg_740['timestamp'] = pd.to_datetime(self.df_agg_740['timestamp'], unit = 's')

    def reset_index(self):
        self.df_agg_740['ts'] = pd.to_datetime(self.df_agg_740['timestamp'], unit = 's')
        self.df_agg_740 = self.df_agg_740.set_index('ts')

    def convert_string_to_datetime64(self, date_string):
        return pd.to_datetime(date_string)

    def filter_data(self, start, end, low, high, convert = False):
        print(f'Filter range, Date: {start} : {end}')
        print(f'Filter range, Temp: {low} : {high}')
        self.start = self.convert_string_to_datetime64(start) if convert else start
        self.end = self.convert_string_to_datetime64(end) if convert else end
        self.low = low
        self.high = high
        return (self.filter_data_based_on_timestamp_and_ecu_temperature(), self.filter_data_based_on_timestamp_and_ecu_temperature(True))

    def filter_data_based_on_timestamp_and_ecu_temperature(self, reverse = False):
        if not reverse:
            return self.df_agg_740[(self.df_agg_740.timestamp >= self.start) &
                (self.df_agg_740.timestamp <= self.end) & (self.df_agg_740.ECU_Temperature >= self.low) &
                (self.df_agg_740.ECU_Temperature <= self.high)]
        else:
            return self.df_agg_740[(self.df_agg_740.timestamp <= self.low) &
                (self.df_agg_740.timestamp >= self.high) &
                (self.df_agg_740.ECU_Temperature <= self.low) &
                (self.df_agg_740.ECU_Temperature >= self.high)]
