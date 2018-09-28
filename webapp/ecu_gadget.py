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
        df_agg_740 = pd.read_csv(files[0])
        df_agg_714 = pd.read_csv(files[1])
        df_agg_740 = pd.concat([df_agg_740,df_agg_714])
        return df_agg_740

    def convert_timestamp(self):
        self.df_agg_740['timestamp'] = pd.to_datetime(self.df_agg_740['timestamp'], unit = 's')

    def reset_index(self):
        self.df_agg_740['ts'] = pd.to_datetime(self.df_agg_740['timestamp'], unit = 's')
        self.df_agg_740 = self.df_agg_740.set_index('ts')

    def convert_string_to_datetime64(self, date_string):
        return pd.to_datetime(date_string)

    def filter_data(self, low, high):
        print(f"{low} - {high}")
        self.low = low
        self.high = high
        df_filtered = self.filter_data_based_on_ecu_temperature()
        df_filtered_outside_interval = self.other_interval_temperature()
        return (df_filtered, df_filtered_outside_interval)

    def filter_data_based_on_ecu_temperature(self):
            return self.df_agg_740[(self.df_agg_740.ECU_Temperature >= self.low) &
                (self.df_agg_740.ECU_Temperature <= self.high)]

    def other_interval_temperature(self):
        return self.df_agg_740[(self.df_agg_740.ECU_Temperature < self.low) |
                (self.df_agg_740.ECU_Temperature > self.high)]

    def filter_data_based_on_timestamp(self):
            return self.df_agg_740[(self.df_agg_740.timestamp >= self.start) &
                (self.df_agg_740.ECU_Temperature <= self.end)]

    def other_interval_timestamp(self):
        return self.df_agg_740[(self.df_agg_740.timestamp < self.start) |
                (self.df_agg_740.timestamp > self.end)]

    def get_vehicle_percentage_above_normal_for_time_window(self, start, end):
        normal = 90
        self.start = start
        self.end = end
        df = self.filter_data_based_on_timestamp()
        df = df[df.ECU_Temperature > normal]
        percentage_above_normal = (len(df) / len(self.df_agg_740)) * 100.0
        percentage_normal = 100.0 - percentage_above_normal
        return (percentage_above_normal, percentage_normal)

    def get_vehicle_details_above_normal_for_time_window(self, start, end):
        normal = 90
        self.start = start
        self.end = end
        df = self.filter_data_based_on_timestamp()
        df = df[df.ECU_Temperature > normal]
        return df[['Vehicle_Number', 'timestamp', 'ECU_Temperature']]
