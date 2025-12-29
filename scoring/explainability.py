def explain(sig):
    return {
        "Hiring Momentum": "Positive" if sig["momentum"] > 0 else "Flat",
        "Role Diversity": sig["role_diversity"],
        "Leadership Hiring": "Yes" if sig["seniority"] > 0 else "No",
        "Tech Signals": sig["tech_signals"],
        "Evidence Strength": (
            "High" if sig["momentum"] > 0 and sig["role_diversity"] >= 3
            else "Medium"
        )
    }
