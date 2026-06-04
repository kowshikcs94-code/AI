from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

features = [
    "ai_adoption_level",
    "automation_rate",
    "ai_investment_usd",
    "employee_ai_training_hours",
    "deployment_count"
]

X = df[features]
y = df["ai_maturity_score"]

X_train,X_test,y_train,y_test = train_test_split(
    X,y,test_size=0.2
)

model = RandomForestRegressor()
model.fit(X_train,y_train)

score = model.score(
    X_test,
    y_test
)

st.metric(
    "Prediction Accuracy",
    f"{score*100:.2f}%"
)
