import pandas as pd
from AlgoFunctions import Algo
import hvplot.pandas
from pandas.core.frame import DataFrame
import matplotlib
import matplotlib.pyplot as plt


def process_df(df, look_back, window_short, window_long):
    df["Current_WR"] = Algo.get_william_r(df["High"], df["Low"], df["Close"], look_back)
    df["Previous_WR"] = df["Current_WR"].shift(periods=look_back)

    # Generate the short and long window simple moving averages (short and long days, respectively)
    df["SMA50"] = df["Close"].rolling(window=window_short).mean()
    df["SMA100"] = df["Close"].rolling(window=window_long).mean()
    df.drop(columns=["Adj Close", 'Volume'], inplace=True)
    return df


def plot_strategy_1(df, name: str, year_list):
    # Slice the plot data with year from the date: get the year out of date
    df['Year'] = pd.to_datetime(df.index).to_period("Y")
    df['Year'] = df['Year'].dt.strftime('%Y')
    df = df[df["Year"].isin(year_list)]

    # Visualize exit_point position relative to close price
    exit_point = df[df['Entry/Exit_S1'] < 0.0][['Close', 'Year']].hvplot.scatter(
        y="Close",
        color='red',
        marker='v',
        size=200,
        legend=False,
        ylabel='Price in $',
        width=1000,
        height=400,
    )

    # Visualize entry position relative to close price
    entry = df[df['Entry/Exit_S1'] > 0.0][['Close', 'Year']].hvplot.scatter(
        y="Close",
        color='green',
        marker='^',
        size=200,
        legend=False,
        ylabel='Price in $',
        width=1000,
        height=400,
    )

    df_close = df[['Close', 'Year']].hvplot(
        y="Close",
        line_color='lightgrey',
        ylabel='Price in $',
        width=1000,
        height=400,
    )

    plot = exit_point * entry * df_close
    plot.opts(
        title=name + " BOV Entry and Exit Points with Strategy 1"
    )

    return plot


def plot_strategy_2(df, name: str, year_list):
    # Slice the plot data with year from the date: get the year out of date
    df['Year'] = pd.to_datetime(df.index).to_period("Y")
    df['Year'] = df['Year'].dt.strftime('%Y')
    df = df[df["Year"].isin(year_list)]

    # Visualize exit_point position relative to close price
    exit_point = df[df['Entry/Exit_S2'] < 0.0][['Close', 'Year']].hvplot.scatter(
        y="Close",
        color='red',
        marker='v',
        size=200,
        legend=False,
        ylabel='Price in $',
        width=1000,
        height=400,

    )

    # Visualize entry position relative to close price
    entry = df[df['Entry/Exit_S2'] > 0.0][['Close', 'Year']].hvplot.scatter(
        y="Close",
        color='green',
        marker='^',
        size=200,
        legend=False,
        ylabel='Price in $',
        width=1000,
        height=400,
    )

    df_close = df[['Close', 'Year']].hvplot(
        y="Close",
        line_color='lightgrey',
        ylabel='Price in $',
        width=1000,
        height=400,
    )

    plot = exit_point * entry * df_close
    plot.opts(
        title=name + " BOV Entry and Exit Points with Strategy 2"
    )

    return plot


def plot_strategy_3(df, name: str, year_list):
    df['Year'] = pd.to_datetime(df.index).to_period("Y")
    df['Year'] = df['Year'].dt.strftime('%Y')
    df = df[df["Year"].isin(year_list)]
    exit_point = df[df['Cross Below Range'] == -1]['Close'].hvplot.scatter(
        color='red',
        marker='v',
        size=200,
        legend=False,
        ylabel='Price in $',
        width=1000,
        height=400
    )

    # Visualize entry position relative to close price
    entry = df[df['Cross Above Range'] == 1]['Close'].hvplot.scatter(
        color='green',
        marker='^',
        size=200,
        legend=False,
        ylabel='Price in $',
        width=1000,
        height=400
    )

    btc_close = df[['Close']].hvplot(
        line_color='lightgrey',
        ylabel='Price in $',
        width=1000,
        height=400
    )

    plot = exit_point * entry * btc_close
    plot.opts(
        title=name + " BOV Entry and Exit Points with Strategy 3"
    )

    return plot
