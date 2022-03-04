import numpy as np
import pandas


def vol_breakout(dataframe: pandas.DataFrame, percentage: int):
    # Convert int to Percentage
    multiplier = percentage / 100

    # Calculate the Top and Bottom of the range to determine where positions will be taken
    top_range_calc = dataframe['high'][-1] * multiplier
    bottom_range_calc = dataframe['low'][-1] * multiplier
    top_of_range = dataframe['open'] + top_range_calc
    bottom_of_range = dataframe['open'] - bottom_range_calc

    # Create Columns that hold the number of times a cross happens above the range, and generates a Signal
    dataframe['Top of Range'] = round(top_of_range, 2)
    dataframe['Cross Above Range'] = np.where(dataframe['close'] > round(top_of_range, 2), 1, 0)
    dataframe['Long Signal'] = dataframe['Cross Above Range'].diff()

    dataframe['Bottom of Range'] = round(bottom_of_range, 2)
    dataframe['Cross Below Range'] = np.where(dataframe['close'] < round(bottom_of_range, 2), 2, 0)
    dataframe['Short Signal'] = dataframe['Cross Below Range'].diff()

    signal_dict = {
        2: 'short',
        -2: 'exit',
        1: 'long',
        -1: 'exit',
        0: 'none'
    }

    dataframe['Long Signal'] = dataframe['Long Signal'].map(signal_dict)
    dataframe['Short Signal'] = dataframe['Short Signal'].map(signal_dict)

    return dataframe
