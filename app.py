import streamlit as st
from pathlib import Path
from VolatilityBreakout import vol_breakout


def read_markdown_file(markdown_file):
    return Path(markdown_file).read_text()


# Display the Project info in the sidebar
st.sidebar.title('Project 3: Williams Break-Out Volatility Strategy')
st.sidebar.markdown('---------')

st.sidebar.markdown('## Project Members:')
st.sidebar.markdown('- [Andrew Crawford](https://github.com/Crawnicles)')
st.sidebar.markdown('- [Sam Kohnle](https://github.com/skohnle14)')
st.sidebar.markdown('- [Servontius Turner](https://github.com/ServontiusT)')
st.sidebar.markdown('- [Sylvia Fan](https://github.com/linshuishui)')
st.sidebar.markdown('---------')

nav_select = st.sidebar.selectbox(label='Navigation', options=['About', 'SPY', 'BTC', 'VIX'])

if nav_select == 'About':
    intro_markdown = read_markdown_file("README.md")
    st.markdown(intro_markdown, unsafe_allow_html=True)
    st.sidebar.markdown('[Check out our project on GitHub](https://github.com/Crawnicles/Algo-trading-project)')
elif nav_select == 'SPY':
    st.markdown('# S&P500')
    spy_df = vol_breakout('data/SPY.csv', 25)
    st.write(spy_df)
elif nav_select == 'BTC':
    st.markdown('# Bitcoin')
    btc_df = vol_breakout('data/BTC.csv', 25)
    st.write(btc_df)
elif nav_select == 'VIX':
    st.markdown('# Volatility Index')
    asset_import = ''
    asset_instance = ''
    asset_class = ''
