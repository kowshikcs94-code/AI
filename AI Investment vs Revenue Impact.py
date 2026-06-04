fig = px.scatter(
    df.sample(10000),
    x="ai_investment_usd",
    y="revenue_impact",
    color="industry",
    size="ai_adoption_level",
    title="Investment vs Revenue"
)

st.plotly_chart(
    fig,
    use_container_width=True
)
