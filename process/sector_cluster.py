from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

def cluster_sectors(job_titles, n_clusters=5):
    if len(job_titles) < n_clusters:
        return ["General"] * len(job_titles)

    vec = TfidfVectorizer(stop_words="english")
    X = vec.fit_transform(job_titles)

    model = KMeans(n_clusters=n_clusters, random_state=42)
    labels = model.fit_predict(X)

    return labels.tolist()
