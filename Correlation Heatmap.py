import seaborn as sns
import matplotlib.pyplot as plt

corr = df.select_dtypes(
    include='number'
).corr()

fig, ax = plt.subplots(
    figsize=(10,8)
)

sns.heatmap(
    corr,
    annot=True,
    cmap="coolwarm",
    ax=ax
)

st.pyplot(fig)
