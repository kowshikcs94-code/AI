df["AI_Readiness"] = (
    df["ai_adoption_level"]*0.4 +
    df["automation_rate"]*0.3 +
    (df["ai_maturity_score"]/10)*0.3
)
