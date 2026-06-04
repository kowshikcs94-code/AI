fig = px.histogram(
    df,
    x="productivity_gain",
    nbins=50,
    title="Productivity Gain Distribution"
)

st.plotly_chart(fig)
