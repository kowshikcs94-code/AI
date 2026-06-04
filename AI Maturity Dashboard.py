fig = px.box(
    df,
    x="industry",
    y="ai_maturity_score",
    color="industry"
)

st.plotly_chart(
    fig,
    use_container_width=True
)
