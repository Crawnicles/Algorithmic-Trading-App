import numpy as np
import pandas as pd


def calculate_s1_returns(df, initial_capital, share_size):
    df["Position"] = share_size * np.where(df["Entry/Exit_S1"] > 0.0, 1, (np.where(df["Entry/Exit_S1"] < 0.0, -1, 0)))

    # Multiply share price by entry/exit positions and get the cumulatively sum
    df["Portfolio_Holdings"] = df["Close"] * df["Position"].cumsum()

    # Subtract the initial capital by the portfolio holdings to get the amount of liquid cash in the portfolio
    df["Portfolio_Cash"] = (
        initial_capital - (df["Close"] * df["Position"]).cumsum()
    )

    # Get the total portfolio value by adding the cash amount by the portfolio holdings (or investments)
    df["Portfolio_Total"] = df["Portfolio_Cash"] + df["Portfolio_Holdings"]

    # Calculate the portfolio daily returns
    df["Portfolio_Daily_Returns"] = df["Portfolio_Total"].pct_change()

    # Calculate the cumulative returns
    df["Portfolio Cumulative Returns"] = (1 + df["Portfolio_Daily_Returns"]).cumprod() - 1
    return df

def display_returns(df, strategy_name, name: str, ylim, list_of_years):
    df['Year'] = pd.to_datetime(df.index).to_period("Y")
    df['Year'] = df['Year'].dt.strftime('%Y')
    df = df[df["Year"].isin(list_of_years) ]
    plot = df["Portfolio Cumulative Returns"].hvplot(
    title=name + " Portfolio Cumulative Returns of " + strategy_name, ylim=ylim)
        
    return plot


def calculate_s2_returns(df, initial_capital, share_size):
    df["Position"] = share_size * np.where(df["Entry/Exit_S2"] > 0.0, 1, (np.where(df["Entry/Exit_S2"] <0.0, -1,0))) 

    # Multiply share price by entry/exit positions and get the cumulatively sum
    df["Portfolio_Holdings"] = df["Close"]* df["Position"].cumsum()

    # Subtract the initial capital by the portfolio holdings to get the amount of liquid cash in the portfolio
    df["Portfolio_Cash"] = (
        initial_capital - (df["Close"] * df["Position"]).cumsum()
    )

    # Get the total portfolio value by adding the cash amount by the portfolio holdings (or investments)
    df["Portfolio_Total"] = df["Portfolio_Cash"] + df["Portfolio_Holdings"]

    # Calculate the portfolio daily returns
    df["Portfolio_Daily_Returns"] = df["Portfolio_Total"].pct_change()

    # Calculate the cumulative returns
    df["Portfolio Cumulative Returns"] = (1 + df["Portfolio_Daily_Returns"]).cumprod() - 1

    return df

#Strategy3 backtest
def calculate_s3_returns(df,initial_capital,share_size): 
    df["Position"] = share_size * df['Above Range'].diff()
    # Multiply share price by entry/exit positions and get the cumulatively sum
    df["Portfolio_Holdings"] = df["Close"]* df["Position"].cumsum()

    # Subtract the initial capital by the portfolio holdings to get the amount of liquid cash in the portfolio
    df["Portfolio_Cash"] = (
        initial_capital - (df["Close"] * df["Position"]).cumsum()
    )

    # Get the total portfolio value by adding the cash amount by the portfolio holdings (or investments)
    df["Portfolio_Total"] = df["Portfolio_Cash"] + df["Portfolio_Holdings"]

    # Calculate the portfolio daily returns
    df["Portfolio_Daily_Returns"] = df["Portfolio_Total"].pct_change()

    # Calculate the cumulative returns
    df["Portfolio Cumulative Returns"] = (1 + df["Portfolio_Daily_Returns"]).cumprod() - 1
    
    return df