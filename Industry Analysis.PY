industry_df = df.groupby(
    "industry"
).agg({
    "ai_adoption_level":"mean",
    "revenue_impact":"sum",
    "cost_savings":"sum"
}).reset_index()

fig = px.bar(
    industry_df,
    x="industry",
    y="ai_adoption_level",
    color="revenue_impact",
    title="Industry AI Adoption"
)

st.plotly_chart(
    fig,
    use_container_width=True
)
