import pandas as pd

def momentum(dates):
    if len(dates) < 6:
        return 0

    try:
        s = pd.Series(1, index=pd.to_datetime(dates))
        m = s.resample("ME").sum()
    except (ValueError, TypeError):
        return 0

    recent = m[-6:].mean()
    earlier = m[:-6].mean() if len(m) > 6 else 0

    if earlier == 0:
        return recent
    return (recent - earlier) / earlier
