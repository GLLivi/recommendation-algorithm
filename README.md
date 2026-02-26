# Cosine Recommender

Projeto de recomendacao de filmes baseado em similaridade do cosseno entre usuarios.

## Sobre este projeto

Este projeto foi feito com intuito didatico para mim: praticar programacao e Data Science, saindo do "so teoria" para uma implementacao real ponta a ponta.

Eu quis manter tudo simples e transparente, sem esconder a matematica por tras. A ideia aqui nao e "modelo de producao", e sim aprendizado pratico com dados reais.

## Como organizei os arquivos (e por que)

Eu decidi separar em 2 arquivos Python para ficar mais facil de entender e executar:

- `main.py`: fluxo principal da execucao (carrega config, le CSVs, chama as funcoes e imprime resultados).
- `recommender.py`: funcoes matematicas do recomendador (similaridade, vizinhos e score).

Essa separacao me ajuda a evoluir o projeto com mais clareza: execucao de um lado, funcoes reutilizaveis do outro.

## Como o algoritmo funciona

### 1) Montagem da matriz usuario x filme

Com `ratings.csv`, o codigo cria uma matriz `R`:

- linha = usuario
- coluna = filme
- valor = nota dada

Se um usuario nao avaliou um filme, fica `NaN`.

### 2) Centralizacao por media do usuario

Para comparar usuarios de forma mais justa, o codigo centraliza as notas por usuario:

\[
r'_{u,i} = r_{u,i} - \bar{r}_u
\]

Onde:
- \(r_{u,i}\): nota do usuario \(u\) no filme \(i\)
- \(\bar{r}_u\): media de notas do usuario \(u\)

Isso reduz o efeito de usuarios que sempre avaliam muito alto ou muito baixo.

### 3) Similaridade do cosseno entre usuarios

A similaridade entre usuario alvo \(u\) e outro usuario \(v\) e:

\[
\text{sim}(u,v) = \frac{\sum_{i \in I_{uv}} r'_{u,i} \cdot r'_{v,i}}
{\sqrt{\sum_{i \in I_{uv}} (r'_{u,i})^2} \cdot \sqrt{\sum_{i \in I_{uv}} (r'_{v,i})^2}}
\]

Onde \(I_{uv}\) e o conjunto de filmes avaliados pelos dois.

No codigo:
- so considera par com pelo menos `min_coinc` filmes em comum;
- so guarda similaridade positiva (`sim > 0`);
- seleciona os `k_neighbors` melhores vizinhos.

### 4) Score de recomendacao por media ponderada

Para cada filme candidato, o score e calculado com as notas dos vizinhos ponderadas pela similaridade:

\[
\text{score}(i) =
\frac{\sum_{v \in N} \text{sim}(u,v)\cdot r_{v,i}}
{\sum_{v \in N} |\text{sim}(u,v)|}
\]

Na implementacao atual, como so entram similaridades positivas, o denominador vira a soma simples dos pesos validos.

Depois, o codigo ordena por score e retorna os `k_recs` melhores filmes.

## Requisitos

- Python 3.12+
- Dependencias:

```bash
pip install -r requirements.txt
```

## Como usar

1. Ajuste `config.json` se quiser trocar usuario ou hiperparametros.
2. Rode:

```bash
python main.py
```

## Parametros do `config.json`

- `ratings_path`: caminho do CSV de avaliacoes.
- `movies_path`: caminho do CSV de filmes.
- `user_id`: usuario alvo.
- `k_neighbors`: quantidade de vizinhos usados.
- `k_recs`: quantidade de recomendacoes finais.
- `min_coinc`: minimo de filmes em comum para comparar dois usuarios.
