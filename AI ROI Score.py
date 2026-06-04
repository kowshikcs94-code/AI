df["ROI"] = (
    df["revenue_impact"]
    + df["cost_savings"]
) / df["ai_investment_usd"]
