# Cosine Recommender

Projeto simples de recomendação de filmes usando similaridade do cosseno entre usuários.

## Propósito

Dado um `user_id`, o programa:
- encontra os usuários mais similares (vizinhos);
- calcula score de recomendação para filmes;
- exibe as top recomendações com título.

## Estrutura

- `main.py`: leitura de configuração e execução do fluxo principal.
- `recommender.py`: funções de similaridade, vizinhança e score.
- `config.json`: parâmetros da execução.
- `data/`: arquivos CSV de entrada (`ratings.csv` e `movies.csv`).

## Requisitos

- Python 3.12+
- Dependências:

```bash
pip install -r requirements.txt
```

## Como usar

1. Ajuste os parâmetros em `config.json` se necessário.
2. Execute:

```bash
python main.py
```

## Parâmetros principais (`config.json`)

- `ratings_path`: caminho para o CSV de avaliações.
- `movies_path`: caminho para o CSV de filmes.
- `user_id`: usuário alvo para recomendação.
- `k_neighbors`: quantidade de vizinhos.
- `k_recs`: quantidade de recomendações.
- `min_coinc`: mínimo de filmes em comum para considerar similaridade.
