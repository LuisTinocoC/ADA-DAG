import networkx as nx
from Graficar import VisualizadorDFS

# Implementación del camino más largo en un DAG utilizando tres enfoques: recursivo, memoización y programación dinámica

# Enfoque Recursivo Básico
def camino_mas_largo_recursivo(grafo, v, visitado):
    visitado[v] = True
    longitud_maxima = 0
    for vecino in grafo[v]:
        if not visitado[vecino]:
            longitud_maxima = max(longitud_maxima, 1 + camino_mas_largo_recursivo(grafo, vecino, visitado))
    visitado[v] = False
    return longitud_maxima

def encontrar_camino_mas_largo_recursivo(grafo):
    n = len(grafo)
    camino_maximo = 0
    for v in range(n):
        visitado = [False] * n
        camino_maximo = max(camino_maximo, camino_mas_largo_recursivo(grafo, v, visitado))
    return camino_maximo

# Enfoque con Memoización
def camino_mas_largo_memo(grafo, v, memo):
    if memo[v] is not None:
        return memo[v]
    longitud_maxima = 0
    for vecino in grafo[v]:
        longitud_maxima = max(longitud_maxima, 1 + camino_mas_largo_memo(grafo, vecino, memo))
    memo[v] = longitud_maxima
    return longitud_maxima

def encontrar_camino_mas_largo_memo(grafo):
    n = len(grafo)
    camino_maximo = 0
    memo = [None] * n
    for v in range(n):
        camino_maximo = max(camino_maximo, camino_mas_largo_memo(grafo, v, memo))
    return camino_maximo

# Enfoque con Programación Dinámica
def encontrar_camino_mas_largo_dp(grafo):
    n = len(grafo)
    grado_entrada = [0] * n
    for u in grafo:
        #print(u)
        for v in u:
            grado_entrada[v] += 1
    
    orden_topologico = []
    pila = [v for v in range(n) if grado_entrada[v] == 0]
    
    while pila:
        u = pila.pop()
        orden_topologico.append(u)
        for v in grafo[u]:
            grado_entrada[v] -= 1
            if grado_entrada[v] == 0:
                pila.append(v)
    
    dist = [-float('inf')] * n
    dist[orden_topologico[0]] = 0
    
    for u in orden_topologico:
        for v in grafo[u]:
            if dist[u] != -float('inf'):
                dist[v] = max(dist[v], dist[u] + 1)
    
    return max(dist)

# Ejemplo de uso
'''
grafo = {
    0: [1, 2],
    1: [2, 3],
    2: [3],
    3: [4],
    4: []
}
'''

#print("============================================")
print("         LEER EL GRAFO")
N = int(input("Ingrese el número de nodos: "))
Grafo = [[] for k in range(N)]
V = int(input("Ingrese el número de vertices: "))
print("LEER LOS VERTICES")
for k in range(V):
    print("---------------------------")
    print("vertice", k+1)
    a = int(input("Nodo Inicio: "))
    b = int(input("Nodo fin: "))
    Grafo[a].append(b)

print("Camino más largo (Recursivo):", encontrar_camino_mas_largo_recursivo(Grafo))
print("Camino más largo (Memoización):", encontrar_camino_mas_largo_memo(Grafo))
print("Camino más largo (Programación Dinámica):", encontrar_camino_mas_largo_dp(Grafo))

# Crear el grafo en NetworkX para visualización
G = nx.DiGraph()
for u in range(N):
    for v in Grafo[u]:
        G.add_edge(u, v)

vis_dfs = VisualizadorDFS(G)
vis_dfs.ejecutar()