import numpy as np
import pandas as pd


def vol_breakout(dataframe, percentage: int):
    # Convert csv file into Dataframe
    dataframe = pd.read_csv(dataframe)

    # Calculate the Top and Bottom of the range to determine where positions will be taken
    top_range_calc = (dataframe.iloc[-1]['High'] * percentage) / 100
    bottom_range_calc = (dataframe.iloc[-1]['Low'] * percentage) / 100
    top_of_range = dataframe['Open'] + top_range_calc
    bottom_of_range = dataframe['Open'] - bottom_range_calc

    # Create Columns that hold the number of times a cross happens above the range, and generates a Signal
    dataframe['Top of Range'] = round(top_of_range, 2)
    dataframe['Cross Above Range'] = np.where(dataframe['Close'] > round(top_of_range, 2), 1, 0)
    dataframe['Long Signal'] = dataframe['Cross Above Range'].diff()

    dataframe['Bottom of Range'] = round(bottom_of_range, 2)
    dataframe['Cross Below Range'] = np.where(dataframe['Close'] < round(bottom_of_range, 2), 2, 0)
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
