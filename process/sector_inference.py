SECTOR_MAP = {
    "fintech": ["bank", "payment", "fintech", "financial"],
    "telecom": ["telecom", "network", "5g"],
    "healthcare": ["health", "medical", "hospital", "pharma"],
    "manufacturing": ["manufacturing", "factory", "industrial", "production"],
    "energy": ["energy", "oil", "gas", "renewable"],
    "ecommerce": ["ecommerce", "retail", "shopping"],
    "logistics": ["logistics", "supply", "warehouse"],
    "software": ["software", "platform", "cloud", "saas"]
}

def infer_sector(roles):
    text = " ".join(roles).lower()

    for sector, keywords in SECTOR_MAP.items():
        for kw in keywords:
            if kw in text:
                return sector.title()

    return "General"
