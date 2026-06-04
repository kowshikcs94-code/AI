country_df = df.groupby(
    "country"
)["ai_adoption_level"].mean().reset_index()

fig = px.choropleth(
    country_df,
    locations="country",
    locationmode="country names",
    color="ai_adoption_level",
    title="Global AI Adoption"
)

st.plotly_chart(fig)
