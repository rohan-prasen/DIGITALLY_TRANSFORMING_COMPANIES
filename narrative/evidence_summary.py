def generate_evidence_summary(company):
    sig = company.get("signals", {})
    name = company.get("name")
    sector = company.get("sector", "Unknown")
    stage = company.get("stage", "Unknown")

    timeline = sig.get("timeline", [])
    roles = sig.get("roles", [])
    tech = sig.get("tech_signals", [])
    seniority = sig.get("seniority", 0)
    momentum = sig.get("momentum", 0)

    total_roles = sum(p["count"] for p in timeline) if timeline else 0
    months_active = len(timeline)

    summary = []

    # 1. Time-based hiring evidence
    if months_active >= 6:
        summary.append(
            f"The company shows sustained digital hiring activity over the last {months_active} months "
            f"with {total_roles} relevant roles posted in the recent period."
        )
    else:
        summary.append(
            f"The company shows limited but recent digital hiring activity ({months_active} months observed)."
        )

    # 2. Role nature
    if roles:
        summary.append(
            f"Key roles include {', '.join(roles[:4])}, indicating focus on digital and technology capabilities."
        )

    # 3. Seniority progression
    if seniority > 0:
        summary.append(
            "The presence of senior or leadership-level technology roles suggests organizational-level "
            "digital ownership rather than isolated experimentation."
        )
    else:
        summary.append(
            "Most roles are execution-level, indicating early or mid-stage digital capability building."
        )

    # 4. Technology signals
    if tech:
        summary.append(
            f"Job descriptions reference modern technologies and platforms such as {', '.join(tech[:4])}, "
            "which are commonly associated with digital transformation initiatives."
        )

    # 5. Momentum
    if momentum > 0:
        summary.append(
            "Hiring momentum shows an upward or sustained trend, suggesting that digital initiatives "
            "are ongoing rather than concluded."
        )
    else:
        summary.append(
            "Hiring momentum appears stable, which may indicate consolidation after recent transformation."
        )

    # 6. Final synthesis
    summary.append(
        f"Based on combined hiring patterns, role composition, and technology signals, "
        f"the company is classified as **{stage}** within the **{sector}** sector."
    )

    return " ".join(summary)
