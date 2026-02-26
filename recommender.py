import pandas as pd
import numpy as np


def cosine_from_series(ru, rv, min_coinc):
    mask = ru.notna() & rv.notna()
    if mask.sum() < min_coinc:
        return 0.0

    a = ru[mask].to_numpy(dtype=float)
    b = rv[mask].to_numpy(dtype=float)

    den = np.linalg.norm(a) * np.linalg.norm(b)
    if den == 0:
        return 0.0

    return float((a @ b) / den)


def top_K_neighbors(R, k, user_id, min_coinc):
    R_mean = R.mean(axis=1, skipna=True)

    ru = R.loc[user_id]
    ru_centr = ru - R_mean.loc[user_id]

    sims = {}
    for other_id in R.index:
        if other_id == user_id:
            continue

        rv = R.loc[other_id]
        rv_centr = rv - R_mean.loc[other_id]

        sim = cosine_from_series(ru_centr, rv_centr, min_coinc)
        if sim > 0:
            sims[other_id] = sim

    if not sims:
        return pd.Series(dtype=float)

    return pd.Series(sims).sort_values(ascending=False).head(k)


def movie_recomend_score(R, k, neighbors):
    if neighbors is None or len(neighbors) == 0:
        return pd.Series(dtype=float)

    ratings_vizinhos = R.loc[neighbors.index]

    num = ratings_vizinhos.mul(neighbors, axis=0).sum(axis=0, skipna=True)
    den = ratings_vizinhos.notna().mul(neighbors, axis=0).sum(axis=0)

    score = num.div(den.replace(0, np.nan)).dropna()
    return score.sort_values(ascending=False).head(k)


def attach_movie_titles(movies_df, movies_score):
    df_score = movies_score.rename("score").reset_index()
    df_score.columns = ["movieId", "score"]
    return df_score.merge(movies_df[["movieId", "title"]], on="movieId", how="left")
