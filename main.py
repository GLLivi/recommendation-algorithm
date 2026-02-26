import json
import pandas as pd
from pathlib import Path

from recommender import (
    top_K_neighbors,
    movie_recomend_score,
    attach_movie_titles,
)

DEFAULT_CONFIG_PATH = "config.json"

def load_config(path=DEFAULT_CONFIG_PATH):
    try:
        config_path = Path(path)
        if not config_path.is_absolute():
            config_path = Path(__file__).resolve().parent / config_path

        with open(config_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)

        _ = cfg["ratings_path"]
        _ = cfg["movies_path"]
        _ = cfg["user_id"]
        _ = cfg["k_neighbors"]
        _ = cfg["k_recs"]
        _ = cfg["min_coinc"]

        return cfg

    except FileNotFoundError:
        print("Erro: não encontrei o config.json.")
        raise SystemExit(1)

    except json.JSONDecodeError:
        print("Erro: config.json inválido (JSON mal formatado).")
        raise SystemExit(1)

    except Exception:
        print("Erro: config.json incompleto ou com algum valor inválido.")
        raise SystemExit(1)


def run_from_config(config_path=DEFAULT_CONFIG_PATH):
    cfg = load_config(config_path)

    df_ratings = pd.read_csv(cfg["ratings_path"])
    df_movies = pd.read_csv(cfg["movies_path"])

    R = df_ratings.pivot(index="userId", columns="movieId", values="rating")

    neighbors = top_K_neighbors(
        R=R,
        k=int(cfg["k_neighbors"]),
        user_id=int(cfg["user_id"]),
        min_coinc=int(cfg["min_coinc"]),
    )

    scores = movie_recomend_score(
        R=R,
        k=int(cfg["k_recs"]),
        neighbors=neighbors,
    )

    result = attach_movie_titles(df_movies, scores)

    pd.set_option("display.width", 120)

    print(
        f"\nUser: {cfg['user_id']} | neighbors: {cfg['k_neighbors']} | recs: {cfg['k_recs']} | min_coinc: {cfg['min_coinc']}"
    )

    if len(neighbors) == 0:
        print("\nNenhum vizinho encontrado com similaridade > 0 (ou poucos filmes em comum).")
        return result

    print("\nTop vizinhos (userId -> sim):")
    print(neighbors.to_string())

    if len(result) == 0:
        print("\nSem recomendações (talvez ninguém avaliou esses filmes dentro do recorte).")
        return result

    print("\nTop recomendações:")
    print(result.to_string(index=False))

    return result


if __name__ == "__main__":
    run_from_config(DEFAULT_CONFIG_PATH)
