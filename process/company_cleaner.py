def is_valid_company(name):
    bad_terms = ["*", "confidential", "recruitment", "staffing"]
    name_l = name.lower()
    if len(name.strip()) < 3:
        return False
    if any(b in name_l for b in bad_terms):
        return False
    return True
