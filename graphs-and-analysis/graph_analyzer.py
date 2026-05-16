import pandas as pd
import networkx as nx
from collections import Counter
import json
import os
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

#caminho dos dados finais relativo ao script
script_dir = os.path.dirname(os.path.abspath(__file__))
DADOS_PATH = os.path.join(script_dir, "../etl/DADOS_FINAIS")


def carregar_dados():
    filmes_df = pd.read_csv(f"{DADOS_PATH}/MOVIES_FINAL.csv")
    atores_df = pd.read_csv(f"{DADOS_PATH}/ACTORS_FINAL.csv")
    movie_actors_df = pd.read_csv(f"{DADOS_PATH}/MOVIE_ACTORS_FINAL.csv")
    generos_df = pd.read_csv(f"{DADOS_PATH}/GENRES_FINAL.csv")
    movie_generos_df = pd.read_csv(f"{DADOS_PATH}/MOVIE_GENRES_FINAL.csv")
    
    print(f"Filmes carregados: {len(filmes_df)}")
    print(f"Atores carregados: {len(atores_df)}")
    print(f"Arestas carregadas: {len(movie_actors_df)}")
    
    return filmes_df, atores_df, movie_actors_df, generos_df, movie_generos_df


def criar_grafo_bipartido(filmes_df, atores_df, movie_actors_df, generos_df, movie_generos_df):
    G = nx.Graph()
    
    #criar mapa de genre_id -> genre_name
    genre_map = dict(zip(generos_df['genre_id'], generos_df['genre_name']))
    
    #criar mapa de movie_id -> lista de gêneros
    movie_generos_map = {}
    for _, row in movie_generos_df.iterrows():
        movie_id = row['movie_id']
        genre_id = row['genre_id']
        genre_name = genre_map.get(genre_id, "Unknown")
        
        if movie_id not in movie_generos_map:
            movie_generos_map[movie_id] = []
        movie_generos_map[movie_id].append(genre_name)
    
    #adicionar nós de filmes
    for _, filme in filmes_df.iterrows():
        movie_id = filme['movie_id']
        generos = movie_generos_map.get(movie_id, [])
        
        G.add_node(
            f"filme_{movie_id}",
            label=filme["title"],
            tipo="filme",
            titulo=filme["title"],
            nota=filme["vote_average"],
            ano=str(filme["release_date"])[:4],
            generos="|".join(generos)  #armazenar como string separada por |
        )
    
    dict_generos_atores = {"female":"feminino", "male":"masculino", "non_binary":"nao_binario", "not_specified":"nao_especificado"}
    #adicionar nós de atores
    for _, ator in atores_df.iterrows():
        G.add_node(
            f"ator_{ator['id']}",
            label=ator["name"],
            tipo="ator",
            nome=ator["name"],
            data_nascimento=ator["birthday"],
            genero = dict_generos_atores[ator["gender"]],
            local_nascimento = ator["place_of_birth"]
        )
    
    #adicionar arestas usando a tabela de relacionamento
    for _, aresta in movie_actors_df.iterrows():
        filme_id = aresta["movie_id"]
        ator_id = aresta["actor_id"]
        
        #obter a nota do filme para usar como peso da aresta
        nota = filmes_df[filmes_df["movie_id"] == filme_id]["vote_average"].values
        peso = nota[0] if len(nota) > 0 else 0
        
        #adicionar aresta
        G.add_edge(
            f"filme_{filme_id}",
            f"ator_{ator_id}",
            peso=peso
        )
    
    return G


def analisar_grafo(G):
    num_vertices = G.number_of_nodes()
    num_arestas = G.number_of_edges()
    
    #calcular grau médio
    graus = [G.degree(node) for node in G.nodes()]
    grau_medio = sum(graus) / len(graus) if graus else 0
    
    #componentes conexas
    componentes = list(nx.connected_components(G))
    num_componentes = len(componentes)
    
    #distribuição de graus
    dist_graus = Counter(graus)
    
    #distribuição de tamanhos das componentes
    tamanhos_componentes = Counter([len(comp) for comp in componentes])
    
    analise = {
        "num_vertices": num_vertices,
        "num_arestas": num_arestas,
        "grau_medio": round(grau_medio, 2),
        "num_componentes": num_componentes,
        "distribuicao_graus": dict(sorted(dist_graus.items())),
        "distribuicao_componentes": dict(sorted(tamanhos_componentes.items())),
        "maior_componente": len(max(componentes, key=len)) if componentes else 0
    }
    
    return analise, componentes


def salvar_grafo_graphml(G, caminho="instancias/grafo_bipartido.graphml"):
    caminho_completo = os.path.join(script_dir, caminho)
    nx.write_graphml(G, caminho_completo)
    print(f"Grafo salvo em {caminho}")


def exibir_analise(analise):
    print()
    print(f"Vértices: {analise['num_vertices']}")
    print(f"Arestas: {analise['num_arestas']}")
    print(f"Grau médio: {analise['grau_medio']}")
    print(f"Componentes conexas: {analise['num_componentes']}")
    print(f"Maior componente: {analise['maior_componente']} nós")
    print()


def visualizar_distribuicao_graus(analise):
    dist_graus = analise['distribuicao_graus']
    graus = sorted([int(k) for k in dist_graus.keys()])
    frequencias = [dist_graus.get(str(g), dist_graus.get(g, 0)) for g in graus]
    
    plt.figure(figsize=(12, 6))
    plt.bar(graus, frequencias, color='steelblue', edgecolor='black', alpha=0.7)
    plt.xlabel('Grau do Nó', fontsize=12)
    plt.ylabel('Número de Nós', fontsize=12)
    plt.title('Distribuição dos Graus do Grafo Bipartido', fontsize=14, fontweight='bold')
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    caminho = os.path.join(script_dir, 'figuras/distribuicao_graus.png')
    plt.savefig(caminho, dpi=300, bbox_inches='tight')
    print("Gráfico de distribuição de graus salvo em 'figuras/distribuicao_graus.png'")
    plt.close()


def visualizar_distribuicao_componentes(analise):
    dist_comp = analise['distribuicao_componentes']
    tamanhos = sorted([int(k) for k in dist_comp.keys()])
    quantidades = [dist_comp.get(str(t), dist_comp.get(t, 0)) for t in tamanhos]
    
    plt.figure(figsize=(12, 6))
    plt.scatter(tamanhos, quantidades, s=200, color='coral', edgecolors='black', alpha=0.7)
    plt.xlabel('Tamanho da Componente (nós)', fontsize=12)
    plt.ylabel('Quantidade de Componentes', fontsize=12)
    plt.title('Distribuição dos Tamanhos das Componentes Conexas', fontsize=14, fontweight='bold')
    plt.xscale('log')
    plt.yscale('log')
    plt.grid(True, alpha=0.3, which='both')
    plt.tight_layout()
    caminho = os.path.join(script_dir, 'figuras/distribuicao_componentes.png')
    plt.savefig(caminho, dpi=300, bbox_inches='tight')
    print("Gráfico de distribuição de componentes salvo em 'figuras/distribuicao_componentes.png'")
    plt.close()


def executar_pipeline():
    #carregando dados
    filmes_df, atores_df, movie_actors_df, generos_df, movie_generos_df = carregar_dados()
    
    #criando grafo bipartido
    G = criar_grafo_bipartido(filmes_df, atores_df, movie_actors_df, generos_df, movie_generos_df)
    
    #analisando grafo
    analise, componentes = analisar_grafo(G)
    exibir_analise(analise)
    
    #gerando visualizações
    visualizar_distribuicao_graus(analise)
    visualizar_distribuicao_componentes(analise)
    
    #salvando grafo
    salvar_grafo_graphml(G)
    
    #salvar análise em json
    caminho_json = os.path.join(script_dir, "instancias/analise_grafo.json")
    with open(caminho_json, "w", encoding="utf-8") as f:
        json.dump(analise, f, indent=2, ensure_ascii=False)
    
    return G, analise, filmes_df, atores_df


if __name__ == "__main__":
    G, analise, filmes, atores = executar_pipeline()
