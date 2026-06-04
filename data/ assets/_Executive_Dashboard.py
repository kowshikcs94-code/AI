import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="AI Adoption Analytics",
    page_icon="🤖",
    layout="wide"
)

@st.cache_data
def load_data():
    return pd.read_csv(
        "data/corporate_ai_adoption_dataset.csv"
    )

df = load_data()

st.title("🤖 Enterprise AI Adoption Dashboard")

col1,col2,col3,col4 = st.columns(4)

col1.metric(
    "Companies",
    f"{len(df):,}"
)

col2.metric(
    "Avg AI Adoption",
    f"{df.ai_adoption_level.mean()*100:.1f}%"
)

col3.metric(
    "Total Investment",
    f"${df.ai_investment_usd.sum()/1e9:.2f}B"
)

col4.metric(
    "Revenue Impact",
    f"${df.revenue_impact.sum()/1e9:.2f}B"
)
