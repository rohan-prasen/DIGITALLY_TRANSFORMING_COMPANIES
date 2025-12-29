def confidence_score(jobs, momentum, role_diversity):
    score = 0
    score += min(len(jobs) / 50, 1) * 40
    score += min(abs(momentum), 1) * 30
    score += min(role_diversity / 5, 1) * 30
    return round(score, 2)
