import streamlit as st
from pathlib import Path
from PlotFunctions import *
from BacktestFunctions import *
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

# Side bar Navigation menu select
nav_select = st.sidebar.selectbox(label='Navigation', options=['About', 'SPY', 'BTC', 'VIX'])

# Dropdown selection of trading strategy
Strategy_select = st.sidebar.selectbox(label='Select Trading Strategy', 
                                       options=['All Strategies','Strategy 1: William%R + SMA&LMA', 'Strategy 2: William%R', 'Strategy 3: VolatilityBreakout'])


# Algo specific Variables
# Define lookback window and percentage:
#lookback = 10
lookback = st.sidebar.slider("Select the lookback days:",min_value =5, max_value=30,value=10)
st.sidebar.write("Lookback days you selected is:", lookback)
# Generate the short and long window simple moving averages (50 and 100 days, respectively)
short_window = 15
long_window = 30

# Set initial capital and initial share size
#initial_capital = float(100000)
initial_capital = float(st.sidebar.number_input("Set the initial capital:", value=100000, min_value= 100))
share_size = -500

# Define the list of years displayed in the Entry/Exit Points Charts
years = ['2017', '2018', '2019', '2020', '2021', '2022']
years = st.sidebar.multiselect(
      'Please select the year(s) you would like to model:',
      ['2017', '2018', '2019', '2020', '2021', '2022'],
      ['2020', '2021',])
st.sidebar.write('You selected:', years)


#Set the percent for algorithm 
percent = float(st.sidebar.number_input("Breakout Percent",min_value= 1,value= 20))
st.sidebar.write("Breakout Percentage you set is:",percent, " %")


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
    if Strategy_select == 'Strategy 1: William%R + SMA&LMA':  
        # Strategy 1
        st.markdown('### Entry/Exit Points')
        spy_strategy_1 = Algo.ma_cross(short_window, spy_processed_df, percent)
        spy_plot_s1 = plot_strategy_1(spy_strategy_1, 'SPY', years)
        st.write(hv.render(spy_plot_s1, backend='bokeh'))
        st.markdown('### Strategy Backtest Result: Portfolio Cumulative Returns')
        spy_return_s1 = calculate_s1_returns(spy_strategy_1,initial_capital,share_size)
        spy_returnplot_s1 = display_returns(spy_return_s1,'William%R + SMA&LMA','SPY',(-1,1),years)
        st.write(hv.render(spy_returnplot_s1,backend='bokeh'))   
        #st.markdown('Place holder text for explanation of visual')
    elif Strategy_select == 'Strategy 2: William%R':
        # Strategy 2
        st.markdown('### Entry/Exit Points')
        spy_strategy_2 = Algo.williams_r(spy_processed_df, percent)
        spy_plot_s2 = plot_strategy_2(spy_strategy_2, 'SPY', years)
        st.write(hv.render(spy_plot_s2, backend='bokeh'))
        st.markdown('### Strategy Backtest Result: Portfolio Cumulative Returns')
        spy_return_s2 = calculate_s2_returns(spy_strategy_2,initial_capital,share_size)
        spy_returnplot_s2 = display_returns(spy_return_s2,'William%R','SPY',(-1,1),years)
        st.write(hv.render(spy_returnplot_s2,backend='bokeh'))   
        #st.markdown('Place holder text for explanation of visual')
    elif Strategy_select == 'Strategy 3: VolatilityBreakout':
        # Strategy 3
        st.markdown('### Entry/Exit Points')        
        spy_strategy_3 = Algo.vol_breakout(spy_processed_df, percent)
        spy_plot_s3 = plot_strategy_3(spy_strategy_3, 'SPY', years)
        st.write(hv.render(spy_plot_s3, backend='bokeh'))
        st.markdown('### Strategy Backtest Result: Portfolio Cumulative Returns')
        spy_return_s3 = calculate_s3_returns(spy_strategy_3,initial_capital,share_size)
        spy_returnplot_s3 = display_returns(spy_return_s3,'VolatilityBreakout','SPY',(-1,1),years)
        st.write(hv.render(spy_returnplot_s3,backend='bokeh'))   
        #st.markdown('Place holder text for explanation of visual')
    elif Strategy_select == 'All Strategies':
        st.markdown('### Entry/Exit Points')
         # Strategy 1
        spy_strategy_1 = Algo.ma_cross(short_window, spy_processed_df, percent)
        spy_plot_s1 = plot_strategy_1(spy_strategy_1, 'SPY', years)
        st.write(hv.render(spy_plot_s1, backend='bokeh'))
         # Strategy 2
        spy_strategy_2 = Algo.williams_r(spy_processed_df, percent)
        spy_plot_s2 = plot_strategy_2(spy_strategy_2, 'SPY', years)
        st.write(hv.render(spy_plot_s2, backend='bokeh'))
        # Strategy 3
        spy_strategy_3 = Algo.vol_breakout(spy_processed_df, percent)
        spy_plot_s3 = plot_strategy_3(spy_strategy_3, 'SPY', years)
        st.write(hv.render(spy_plot_s3, backend='bokeh'))
        st.markdown('### Strategy Backtest Result: Portfolio Cumulative Returns')  
        spy_return_s1 = calculate_s1_returns(spy_strategy_1,initial_capital,share_size)
        spy_returnplot_s1 = display_returns(spy_return_s1,'William%R + SMA&LMA','SPY',(-1,1),years)
        st.write(hv.render(spy_returnplot_s1,backend='bokeh'))         
        spy_return_s2 = calculate_s2_returns(spy_strategy_2,initial_capital,share_size)
        spy_returnplot_s2 = display_returns(spy_return_s2,'William%R','SPY',(-1,1),years)
        st.write(hv.render(spy_returnplot_s2,backend='bokeh'))  
        spy_return_s3 = calculate_s3_returns(spy_strategy_3,initial_capital,share_size)
        spy_returnplot_s3 = display_returns(spy_return_s3,'VolatilityBreakout','SPY',(-1,1),years)
        st.write(hv.render(spy_returnplot_s3,backend='bokeh'))   

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

    if Strategy_select == 'Strategy 1: William%R + SMA&LMA':  
        # Strategy 1
        st.markdown('### Entry/Exit Points')
        btc_strategy_1 = Algo.ma_cross(short_window, btc_processed_df, percent)
        btc_plot_s1 = plot_strategy_1(btc_strategy_1, 'BTC', years)
        st.write(hv.render(btc_plot_s1, backend='bokeh'))
        st.markdown('### Strategy Backtest Result: Portfolio Cumulative Returns')
        btc_return_s1 = calculate_s1_returns(btc_strategy_1,initial_capital,share_size)
        btc_returnplot_s1 = display_returns(btc_return_s1,'William%R + SMA&LMA','BTC',(-500,500),years)
        st.write(hv.render(btc_returnplot_s1,backend='bokeh'))   
        #st.markdown('Place holder text for explanation of visual')
    elif Strategy_select == 'Strategy 2: William%R':
        # Strategy 2
        st.markdown('### Entry/Exit Points')
        btc_strategy_2 = Algo.williams_r(btc_processed_df, percent)
        btc_plot_s2 = plot_strategy_2(btc_strategy_2, 'btc', years)
        st.write(hv.render(btc_plot_s2, backend='bokeh'))
        st.markdown('### Strategy Backtest Result: Portfolio Cumulative Returns')
        btc_return_s2 = calculate_s2_returns(btc_strategy_2,initial_capital,share_size)
        btc_returnplot_s2 = display_returns(btc_return_s2,'William%R','BTC',(-1000,1000),years)
        st.write(hv.render(btc_returnplot_s2,backend='bokeh'))   
        #st.markdown('Place holder text for explanation of visual')
    elif Strategy_select == 'Strategy 3: VolatilityBreakout':
        # Strategy 3
        st.markdown('### Entry/Exit Points')        
        btc_strategy_3 = Algo.vol_breakout(btc_processed_df, percent)
        btc_plot_s3 = plot_strategy_3(btc_strategy_3, 'btc', years)
        st.write(hv.render(btc_plot_s3, backend='bokeh'))
        st.markdown('### Strategy Backtest Result: Portfolio Cumulative Returns')
        btc_return_s3 = calculate_s3_returns(btc_strategy_3,initial_capital,share_size)
        btc_returnplot_s3 = display_returns(btc_return_s3,'VolatilityBreakout','BTC',(-1000,1000),years)
        st.write(hv.render(btc_returnplot_s3,backend='bokeh'))   
        #st.markdown('Place holder text for explanation of visual')
    elif Strategy_select == 'All Strategies':
        st.markdown('### Entry/Exit Points')
         # Strategy 1
        btc_strategy_1 = Algo.ma_cross(short_window, btc_processed_df, percent)
        btc_plot_s1 = plot_strategy_1(btc_strategy_1, 'BTC', years)
        st.write(hv.render(btc_plot_s1, backend='bokeh'))
         # Strategy 2
        btc_strategy_2 = Algo.williams_r(btc_processed_df, percent)
        btc_plot_s2 = plot_strategy_2(btc_strategy_2, 'BTC', years)
        st.write(hv.render(btc_plot_s2, backend='bokeh'))
        # Strategy 3
        btc_strategy_3 = Algo.vol_breakout(btc_processed_df, percent)
        btc_plot_s3 = plot_strategy_3(btc_strategy_3, 'BTC', years)
        st.write(hv.render(btc_plot_s3, backend='bokeh'))
        
        st.markdown('### Strategy Backtest Result: Portfolio Cumulative Returns')  
        btc_return_s1 = calculate_s1_returns(btc_strategy_1,initial_capital,share_size)
        btc_returnplot_s1 = display_returns(btc_return_s1,'William%R + SMA&LMA','BTC',(-500,500),years)
        st.write(hv.render(btc_returnplot_s1,backend='bokeh'))         
        btc_return_s2 = calculate_s2_returns(btc_strategy_2,initial_capital,share_size)
        btc_returnplot_s2 = display_returns(btc_return_s2,'William%R','BTC',(-1000,1000),years)
        st.write(hv.render(btc_returnplot_s2,backend='bokeh'))  
        btc_return_s3 = calculate_s3_returns(btc_strategy_3,initial_capital,share_size)
        btc_returnplot_s3 = display_returns(btc_return_s3,'VolatilityBreakout','BTC',(-1000,1000),years)
        st.write(hv.render(btc_returnplot_s3,backend='bokeh'))   


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

    if Strategy_select == 'Strategy 1: William%R + SMA&LMA':  
        # Strategy 1
        st.markdown('### Entry/Exit Points')
        vix_strategy_1 = Algo.ma_cross(short_window, vix_processed_df, percent)
        vix_plot_s1 = plot_strategy_1(vix_strategy_1, 'VIX', years)
        st.write(hv.render(vix_plot_s1, backend='bokeh'))
        st.markdown('### Strategy Backtest Result: Portfolio Cumulative Returns')
        vix_return_s1 = calculate_s1_returns(vix_strategy_1,initial_capital,share_size)
        vix_returnplot_s1 = display_returns(vix_return_s1,'William%R + SMA&LMA','VIX',(-1,1))
        st.write(hv.render(vix_returnplot_s1,backend='bokeh'))   
        #st.markdown('Place holder text for explanation of visual')
    elif Strategy_select == 'Strategy 2: William%R':
        # Strategy 2
        st.markdown('### Entry/Exit Points')
        vix_strategy_2 = Algo.williams_r(vix_processed_df, percent)
        vix_plot_s2 = plot_strategy_2(vix_strategy_2, 'VIX', years)
        st.write(hv.render(vix_plot_s2, backend='bokeh'))
        st.markdown('### Strategy Backtest Result: Portfolio Cumulative Returns')
        vix_return_s2 = calculate_s2_returns(vix_strategy_2,initial_capital,share_size)
        vix_returnplot_s2 = display_returns(vix_return_s2,'William%R','VIX',(-1,1))
        st.write(hv.render(vix_returnplot_s2,backend='bokeh'))   
        #st.markdown('Place holder text for explanation of visual')
    elif Strategy_select == 'Strategy 3: VolatilityBreakout':
        # Strategy 3
        st.markdown('### Entry/Exit Points')        
        vix_strategy_3 = Algo.vol_breakout(vix_processed_df, percent)
        vix_plot_s3 = plot_strategy_3(vix_strategy_3, 'VIX', years)
        st.write(hv.render(vix_plot_s3, backend='bokeh'))
        st.markdown('### Strategy Backtest Result: Portfolio Cumulative Returns')
        vix_return_s3 = calculate_s3_returns(vix_strategy_3,initial_capital,share_size)
        vix_returnplot_s3 = display_returns(vix_return_s3,'VolatilityBreakout','VIX',(-1,1))
        st.write(hv.render(vix_returnplot_s3,backend='bokeh'))   
        #st.markdown('Place holder text for explanation of visual')
    elif Strategy_select == 'All Strategies':
        st.markdown('### Entry/Exit Points')
         # Strategy 1
        vix_strategy_1 = Algo.ma_cross(short_window, vix_processed_df, percent)
        vix_plot_s1 = plot_strategy_1(vix_strategy_1, 'VIX', years)
        st.write(hv.render(vix_plot_s1, backend='bokeh'))
         # Strategy 2
        vix_strategy_2 = Algo.williams_r(vix_processed_df, percent)
        vix_plot_s2 = plot_strategy_2(vix_strategy_2, 'VIX', years)
        st.write(hv.render(vix_plot_s2, backend='bokeh'))
        # Strategy 3
        vix_strategy_3 = Algo.vol_breakout(vix_processed_df, percent)
        vix_plot_s3 = plot_strategy_3(vix_strategy_3, 'VIX', years)
        st.write(hv.render(vix_plot_s3, backend='bokeh'))
        st.markdown('### Strategy Backtest Result: Portfolio Cumulative Returns')  
        vix_return_s1 = calculate_s1_returns(vix_strategy_1,initial_capital,share_size)
        vix_returnplot_s1 = display_returns(vix_return_s1,'William%R + SMA&LMA','VIX',(-1,1))
        st.write(hv.render(vix_returnplot_s1,backend='bokeh'))         
        vix_return_s2 = calculate_s2_returns(vix_strategy_2,initial_capital,share_size)
        vix_returnplot_s2 = display_returns(vix_return_s2,'William%R','VIX',(-1,1))
        st.write(hv.render(vix_returnplot_s2,backend='bokeh'))  
        vix_return_s3 = calculate_s3_returns(vix_strategy_3,initial_capital,share_size)
        vix_returnplot_s3 = display_returns(vix_return_s3,'VolatilityBreakout','VIX',(-1,1))
        st.write(hv.render(vix_returnplot_s3,backend='bokeh'))   
if st.sidebar.button("Celebration Time!"):
    st.sidebar.balloons()
st.sidebar.markdown('---------')    
st.sidebar.markdown('[Check out our project on GitHub](https://github.com/Crawnicles/Algo-trading-project)')
