class DataProcessor:
    @staticmethod
    def process_data(df):
        # Assuming 'Date' is the index of df and already in the correct datetime format
        data_tuples = list(df.itertuples(index=True, name=None))
        return data_tuples
