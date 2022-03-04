import streamlit as st
from pathlib import Path
from PlotFunctions import *
import holoviews as hv

# Display the Project info in the sidebar
st.sidebar.title('Project 3: Williams Break-Out Volatility Strategy')
st.sidebar.markdown('---------')

st.sidebar.markdown('## Project Members:')
st.sidebar.markdown('- [Andrew Crawford](https://github.com/Crawnicles)')
st.sidebar.markdown('- [Sam Kohnle](https://github.com/skohnle14)')
st.sidebar.markdown('- [Servontius Turner](https://github.com/ServontiusT)')
st.sidebar.markdown('- [Sylvia Fan](https://github.com/linshuishui)')
st.sidebar.markdown('---------')

# Algo specific Variables
# Define lookback window and percentage:
lookback = 10
percent = 20

# Generate the short and long window simple moving averages (50 and 100 days, respectively)
short_window = 15
long_window = 30

# Set initial capital and initial share size
initial_capital = float(100000)
share_size = -500

# Define the list of years displayed in the Entry/Exit Points Charts
years = ['2017', '2018', '2019', '2020', '2021', '2022']

# Side bar Navigation menu select
nav_select = st.sidebar.selectbox(label='Navigation', options=['About', 'SPY', 'BTC', 'VIX'])

if nav_select == 'About':
    intro_markdown = Path("README.md").read_text()
    st.markdown(intro_markdown, unsafe_allow_html=True)

elif nav_select == 'SPY':
    st.markdown('# S&P500')

    # Import SPY market data
    spy_df = pd.read_csv('data/SPY.csv',
                         index_col="Date",
                         parse_dates=True,
                         infer_datetime_format=True
                         )

    # Create Dataframes for plotting
    spy_processed_df = process_df(spy_df, lookback, short_window, long_window)

    # Strategy 1
    spy_strategy_1 = Algo.ma_cross(short_window, spy_processed_df, percent)
    spy_plot_s1 = plot_strategy_1(spy_strategy_1, 'SPY', years)
    st.write(hv.render(spy_plot_s1, backend='bokeh'))
    st.markdown('Place holder text for explanation of visual')

    # Strategy 2
    spy_strategy_2 = Algo.williams_r(spy_processed_df, percent)
    spy_plot_s2 = plot_strategy_2(spy_strategy_2, 'SPY', years)
    st.write(hv.render(spy_plot_s2, backend='bokeh'))
    st.markdown('Place holder text for explanation of visual')

    # Strategy 3
    spy_strategy_3 = Algo.vol_breakout(spy_processed_df, percent)
    spy_plot_s3 = plot_strategy_3(spy_strategy_3, 'SPY', years)
    st.write(hv.render(spy_plot_s3, backend='bokeh'))
    st.markdown('Place holder text for explanation of visual')

elif nav_select == 'BTC':
    st.markdown('# Bitcoin')

    # Import BTC market data
    btc_df = pd.read_csv('data/BTC.csv',
                         index_col="Date",
                         parse_dates=True,
                         infer_datetime_format=True
                         )

    # Create Dataframes for plotting
    btc_processed_df = process_df(btc_df, lookback, short_window, long_window)

    # Strategy 1
    btc_strategy_1 = Algo.ma_cross(short_window, btc_processed_df, percent)
    btc_plot_s1 = plot_strategy_1(btc_strategy_1, 'BTC', years)
    st.write(hv.render(btc_plot_s1, backend='bokeh'))
    st.markdown('Place holder text for explanation of visual')

    # Strategy 2
    btc_strategy_2 = Algo.williams_r(btc_processed_df, percent)
    btc_plot_s2 = plot_strategy_2(btc_strategy_2, 'BTC', years)
    st.write(hv.render(btc_plot_s2, backend='bokeh'))
    st.markdown('Place holder text for explanation of visual')

    # Strategy 3
    btc_strategy_3 = Algo.vol_breakout(btc_processed_df, percent)
    btc_plot_s3 = plot_strategy_3(btc_strategy_3, 'BTC', years)
    st.write(hv.render(btc_plot_s3, backend='bokeh'))
    st.markdown('Place holder text for explanation of visual')

elif nav_select == 'VIX':
    st.markdown('# Volatility Index')
    
    # Import VIX market data
    vix_df = pd.read_csv('data/VIX.csv',
                         index_col="Date",
                         parse_dates=True,
                         infer_datetime_format=True
                         )

    # Create Dataframes for plotting
    vix_processed_df = process_df(vix_df, lookback, short_window, long_window)

    # Strategy 1
    vix_strategy_1 = Algo.ma_cross(short_window, vix_processed_df, percent)
    vix_plot_s1 = plot_strategy_1(vix_strategy_1, 'VIX', years)
    st.write(hv.render(vix_plot_s1, backend='bokeh'))
    st.markdown('Place holder text for explanation of visual')

    # Strategy 2
    vix_strategy_2 = Algo.williams_r(vix_processed_df, percent)
    vix_plot_s2 = plot_strategy_2(vix_strategy_2, 'VIX', years)
    st.write(hv.render(vix_plot_s2, backend='bokeh'))
    st.markdown('Place holder text for explanation of visual')

    # Strategy 3
    vix_strategy_3 = Algo.vol_breakout(vix_processed_df, percent)
    vix_plot_s3 = plot_strategy_3(vix_strategy_3, 'VIX', years)
    st.write(hv.render(vix_plot_s3, backend='bokeh'))
    st.markdown('Place holder text for explanation of visual')

st.sidebar.markdown('[Check out our project on GitHub](https://github.com/Crawnicles/Algo-trading-project)')
