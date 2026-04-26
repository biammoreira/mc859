# 🎬 Otimização Multiobjetivo em Grafos Bipartidos

**MC859 — Projeto em Teoria da Computação**  
Instituto de Computação, Unicamp · 2026

> Encontrar a Fronteira de Pareto que equilibra qualidade e quantidade de filmes necessários para cobrir um subconjunto de atores em um grafo bipartido.

---

## 👥 Equipe

| Nome | RA |
|---|---|
| Maria Beatriz Guimarães Trombini Manhães Moreira | 252873 |
| Mateus de Lima Almeida | 242827 |

---

## 📌 Sobre o Projeto

O projeto modela a relação entre atores e filmes como um **grafo bipartido**, onde:

- **Vértices** representam atores e filmes
- **Arestas** conectam um ator a um filme em que ele participou

O objetivo é resolver um problema de **otimização multiobjetivo**: dado um subconjunto de atores, encontrar um conjunto de filmes que maximize a qualidade média das avaliações e minimize a quantidade de filmes necessários para cobri-los — produzindo a **Fronteira de Pareto** desse trade-off.

---

## 📁 Estrutura do Repositório

```
mc859/
├── etl/
│   └── DADOS_FINAIS/       # Arquivos CSV usados para construção do grafo
├── graphs-and-analysis/
│   └── instancias/
│       └── grafo_bipartido.graphml   # Instância principal do grafo
├── requirements.txt
└── README.md
```

---

## 🗄️ Dataset

Os dados foram coletados entre **15 de março e 4 de abril de 2026** via [TMDB API](https://developer.themoviedb.org/reference), usando três endpoints:

- `/discover/movie` — listagem de filmes (mínimo de 100 votos por filme)
- `/movie/{id}?append_to_response=credits` — detalhes e elenco
- `/person/{id}` — dados dos atores

## 📊 Instância do Grafo

O grafo bipartido final está disponível em formato **GraphML**:

📎 [`graphs-and-analysis/instancias/grafo_bipartido.graphml`](./graphs-and-analysis/instancias/grafo_bipartido.graphml)


## 🛠️ Tecnologias

- **Python 3**
- [NetworkX](https://networkx.org/) — construção e análise do grafo
- [TMDB API](https://developer.themoviedb.org/) — fonte dos dados

Para instalar as dependências:

```bash
pip install -r requirements.txt
```
