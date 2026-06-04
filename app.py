import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Enterprise AI Adoption Dashboard",
    page_icon="🤖",
    layout="wide"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>
.main {
    background-color: #0f172a;
}

.metric-card {
    background-color: #1e293b;
    padding: 15px;
    border-radius: 12px;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

@st.cache_data
def load_data():
    return pd.read_csv(
        "data/corporate_ai_adoption_dataset.csv"
    )

df = load_data()

# --------------------------------------------------
# STANDARDIZE COLUMN NAMES
# --------------------------------------------------

df.columns = (
    df.columns
    .str.lower()
    .str.replace(" ", "_")
)

# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------

st.sidebar.title("⚙ Filters")

industry = st.sidebar.multiselect(
    "Industry",
    sorted(df["industry"].unique()),
    default=sorted(df["industry"].unique())
)

country = st.sidebar.multiselect(
    "Country",
    sorted(df["country"].unique()),
    default=sorted(df["country"].unique())
)

year = st.sidebar.multiselect(
    "Year",
    sorted(df["year"].unique()),
    default=sorted(df["year"].unique())
)

filtered_df = df[
    (df["industry"].isin(industry))
    & (df["country"].isin(country))
    & (df["year"].isin(year))
]

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("🤖 Enterprise AI Adoption Analytics Dashboard")

st.markdown(
    "Analyze AI adoption, investment, maturity, automation, ROI and business impact across industries."
)

# --------------------------------------------------
# KPI SECTION
# --------------------------------------------------

total_records = len(filtered_df)

avg_adoption = filtered_df["ai_adoption_level"].mean()

total_investment = filtered_df["ai_investment_usd"].sum()

total_revenue = filtered_df["revenue_impact"].sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Organizations",
    f"{total_records:,}"
)

col2.metric(
    "Avg Adoption",
    f"{avg_adoption:.2f}"
)

col3.metric(
    "AI Investment",
    f"${total_investment/1e9:.2f}B"
)

col4.metric(
    "Revenue Impact",
    f"${total_revenue/1e9:.2f}B"
)

st.divider()

# --------------------------------------------------
# ROI CALCULATION
# --------------------------------------------------

filtered_df["roi"] = (
    filtered_df["revenue_impact"]
    + filtered_df["cost_savings"]
) / filtered_df["ai_investment_usd"]

# --------------------------------------------------
# AI READINESS INDEX
# --------------------------------------------------

filtered_df["ai_readiness"] = (
    filtered_df["ai_adoption_level"] * 0.4
    + filtered_df["automation_rate"] * 0.3
    + (filtered_df["ai_maturity_score"] / 10) * 0.3
)

# --------------------------------------------------
# CHARTS ROW 1
# --------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    industry_adoption = (
        filtered_df.groupby("industry")
        ["ai_adoption_level"]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        industry_adoption,
        x="industry",
        y="ai_adoption_level",
        title="AI Adoption by Industry",
        color="ai_adoption_level"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    country_readiness = (
        filtered_df.groupby("country")
        ["ai_readiness"]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        country_readiness,
        x="country",
        y="ai_readiness",
        title="AI Readiness by Country",
        color="ai_readiness"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# --------------------------------------------------
# CHARTS ROW 2
# --------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    fig = px.scatter(
        filtered_df.sample(
            min(5000, len(filtered_df))
        ),
        x="ai_investment_usd",
        y="revenue_impact",
        color="industry",
        size="ai_adoption_level",
        title="Investment vs Revenue Impact"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    fig = px.box(
        filtered_df,
        x="industry",
        y="ai_maturity_score",
        color="industry",
        title="AI Maturity Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# --------------------------------------------------
# PRODUCTIVITY ANALYSIS
# --------------------------------------------------

st.subheader("📈 Productivity Gain Distribution")

fig = px.histogram(
    filtered_df,
    x="productivity_gain",
    nbins=40,
    title="Productivity Gain"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# TOP ROI INDUSTRIES
# --------------------------------------------------

st.subheader("🏆 Industry ROI Ranking")

roi_table = (
    filtered_df.groupby("industry")["roi"]
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)

st.dataframe(
    roi_table,
    use_container_width=True
)

# --------------------------------------------------
# YEARLY ADOPTION TREND
# --------------------------------------------------

st.subheader("📊 AI Adoption Trend")

yearly = (
    filtered_df.groupby("year")
    ["ai_adoption_level"]
    .mean()
    .reset_index()
)

fig = px.line(
    yearly,
    x="year",
    y="ai_adoption_level",
    markers=True,
    title="Yearly AI Adoption Growth"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# MACHINE LEARNING
# --------------------------------------------------

st.subheader("🤖 AI Maturity Prediction")

features = [
    "ai_adoption_level",
    "automation_rate",
    "ai_investment_usd",
    "employee_ai_training_hours",
    "deployment_count"
]

if all(col in filtered_df.columns for col in features):

    X = filtered_df[features]
    y = filtered_df["ai_maturity_score"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42
    )

    model.fit(X_train, y_train)

    score = model.score(
        X_test,
        y_test
    )

    st.metric(
        "Model Accuracy (R²)",
        f"{score:.2%}"
    )

# --------------------------------------------------
# EXECUTIVE INSIGHTS
# --------------------------------------------------

st.subheader("💡 Executive Insights")

top_industry = (
    filtered_df.groupby("industry")
    ["ai_adoption_level"]
    .mean()
    .idxmax()
)

top_country = (
    filtered_df.groupby("country")
    ["ai_readiness"]
    .mean()
    .idxmax()
)

st.success(
    f"""
    • Highest AI Adoption Industry: {top_industry}

    • Leading AI Ready Country: {top_country}

    • Total Investment: ${total_investment/1e9:.2f} Billion

    • Average Adoption Score: {avg_adoption:.2f}
    """
)

st.caption(
    "Developed using Streamlit, Plotly, Pandas and Scikit-Learn"
)
