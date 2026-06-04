roi = df.groupby(
    "industry"
)["ROI"].mean()

st.dataframe(
    roi.sort_values(
        ascending=False
    )
)
