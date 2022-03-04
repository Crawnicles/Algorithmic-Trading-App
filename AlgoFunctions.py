import numpy as np
import pandas as pd


class Algo:
    def __init__(self, short_window, long_window):
        self.short_window = short_window
        self.long_window = long_window

    @staticmethod
    def get_william_r(high, low, close, lookback):
        high = high.rolling(lookback).max()
        low = low.rolling(lookback).min()
        wr = -100 * (high - close) / (high - low)

        return wr

    @staticmethod
    def ma_cross(short_window, df, percent: int):
        # Add a new column
        df["WR_BS"] = 0.0
        df["MA_Signal"] = 0.0
        df["MA_BS"] = 0.0
        df["Buy_Sell"] = 0.0
        df["Entry/Exit_S1"] = 0.0
        for index, row in df.iterrows():
            if row["Previous_WR"] < -percent < row["Current_WR"]:
                df.loc[index, "WR_BS"] = 1
            elif row["Previous_WR"] > -(100 - percent) > row["Current_WR"]:
                df.loc[index, "WR_BS"] = 0
        # Generate the trading signal 0 or 1,
        # where 1 is the short-window (SMA50) greater than the long-window (SMA100)
        # and 0 is when the condition is not met
        df["MA_Signal"][short_window:] = np.where(df["SMA50"][short_window:] > df["SMA100"][short_window:], 1.0, 0.0)
        df["MA_BS"] = df["MA_Signal"].diff()
        df["Buy_Sell"] = np.where((df["WR_BS"] + df["MA_Signal"] == 2.0), 1.0, 0.0)
        # Calculate the points in time when the Signal value changes
        # Identify trade entry (1) and exit (-1) points
        df["Entry/Exit_S1"] = df["Buy_Sell"].diff()

        return df

    @staticmethod
    def williams_r(df, percent: int):
        # Add a new column
        df["Buy1_Sell0"] = 0.0
        df["MA_Signal"] = 0.0
        df["Buy_Sell"] = 0.0
        df["Entry/Exit_S2"] = 0.0
        for index, row in df.iterrows():
            if row["Previous_WR"] < -percent < row["Current_WR"]:
                df.loc[index, "Buy1_Sell0"] = 1.0
            elif row["Previous_WR"] > -(100 - percent) > row["Current_WR"]:
                df.loc[index, "Buy1_Sell0"] = -1.0
        # Calculate the points in time when the Signal value changes
        # Identify trade entry (1) and exit (-1) points
        df["Entry/Exit_S2"] = df["Buy1_Sell0"].diff()

        return df

    @staticmethod
    def vol_breakout(dataframe, percentage: int):
        """
        This method is for the Volatility Breakout Strategy where-in an expected percent move is provided and signals
        are generated once the target has been reached.

        :param dataframe: Accepts CSV file or Dataframe containing market data [Open, High, Low, Close].
        :param percentage: Percent move expected
        :return: Returns a Pandas Dataframe
        """
        # Calculate the Top and Bottom of the range to determine where positions will be taken
        top_range_calc = (dataframe.iloc[1]['High'] * percentage) / 100
        bottom_range_calc = (dataframe.iloc[1]['Low'] * percentage) / 100
        top_of_range = dataframe['Open'] + top_range_calc.round()
        bottom_of_range = dataframe['Open'] - bottom_range_calc

        # Create Columns that hold the number of times a cross happens above the range, and generates a Signal
        dataframe['Top of Range'] = top_of_range
        dataframe['Cross Above Range'] = np.where(dataframe['Close'] > top_of_range, 1, 0)
        dataframe['Long Signal'] = dataframe['Cross Above Range'].diff()

        dataframe['Bottom of Range'] = bottom_of_range
        dataframe['Cross Below Range'] = np.where(dataframe['Close'] < bottom_of_range, -1, 0)
        dataframe['Short Signal'] = dataframe['Cross Below Range'].diff()
        # Find the columns where a cross happens and updates the column with a 1 if there is a cross
        dataframe['Above Range'] = np.where(dataframe['Close'] > round(top_of_range, 2), 1, 0)
        dataframe['Below Range'] = np.where(dataframe['Close'] < round(bottom_of_range, 2), 1, 0)
  #return(df)

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
