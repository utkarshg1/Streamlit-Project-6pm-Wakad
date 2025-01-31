import streamlit as st
from client import StockAPI

# Setup the page with tile
st.set_page_config(page_title="Stock Market App", layout="wide")

@st.cache_resource(ttl=3600)
def fetch_client():
    return StockAPI()

stock_api = fetch_client()

@st.cache_data(ttl=3600)
def get_symbols(company: str) -> dict:
    symbols = stock_api.symbol_search(company)
    return symbols

@st.cache_data(ttl=3600)
def plot_chart(symbol: str):
    df = stock_api.daily_data(symbol)
    fig = stock_api.plotly_chart(df)
    return fig

# Add a title to webpage
st.title("Stock Market App")

# Add a subheading showing author name
st.subheader("by Utkarsh Gaikwad")

# Add a company name input box
company = st.text_input("Company Name")

# Create a dropdown for symbol search
if company:
    company_data = get_symbols(company)
    
    if company_data:
        symbols = list(company_data.keys())
        options = st.selectbox("Select Stock Symbol", symbols)
        selected_data = company_data.get(options)
        st.success(f"Company Name : {selected_data[0]}")
        st.success(f"Country / Region : {selected_data[1]}")
        st.success(f"Currency : {selected_data[2]}")
        # Create a button
        submit = st.button("plot", type="primary")
        # If button is clicked
        if submit:
            fig = plot_chart(options)
            st.plotly_chart(fig)
    else:
        st.error("The given company name does not exist")
