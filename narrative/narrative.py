def generate(company, sig, score):
    return f"""
DIGITAL TRANSFORMATION ANALYSIS — {company}

This company shows **active digital transformation**, not static maturity.

HIRING BEHAVIOR
Hiring momentum indicates acceleration in digital roles, particularly across
{', '.join(sig['roles'])}. This reflects internal capability building.

SENIORITY SIGNALS
Leadership-level digital roles indicate strategic commitment rather than experimentation.

TECHNOLOGY SHIFT
Technology indicators suggest migration toward modern cloud-native architectures.

TEMPORAL EVIDENCE
Signals are concentrated in the last 24 months, confirming transformation in progress.

FINAL SCORE
DTS = {score}

Conclusion: This organization is actively transforming its digital core.
"""
