def compute_dts(sig):
    """
    Digital Transformation Score (DTS)

    Uses only signals that actually exist in `sig`.
    """

    score = 0

    # Hiring acceleration (strongest signal)
    score += sig["momentum"] * 35

    # Breadth of digital roles
    score += sig["role_diversity"] * 10

    # Senior leadership hires
    score += sig["seniority"] * 15

    # Technology direction (from job titles)
    tech_strength = len(sig.get("tech_signals", []))
    score += tech_strength * 10

    return round(score, 2)
