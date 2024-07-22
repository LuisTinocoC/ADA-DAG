import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

class VisualizadorDFS:
    def __init__(self, grafo):
        self.G = grafo
        self.tiempo = 0
        self.visitados = set()
        self.pila = []
        self.pasos = []
        self.paso_actual = 0
        self.pos = nx.spring_layout(self.G) 

        # Preparar el grafo
        for nodo in self.G.nodes():
            self.G.nodes[nodo]['color'] = 'white'
            self.G.nodes[nodo]['descubrimiento'] = 0
            self.G.nodes[nodo]['finalización'] = 0

        # Ejecutar DFS y guardar pasos
        for nodo in self.G.nodes():
            if self.G.nodes[nodo]['color'] == 'white':
                self.visitar_dfs(nodo)

        # Crear interfaz gráfica
        self.root = tk.Tk()
        self.root.title("Visualizador DFS")

        # Crear figura de matplotlib
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Crear botones
        frame_botones = tk.Frame(self.root)
        frame_botones.pack(side=tk.BOTTOM)

        self.boton_anterior = tk.Button(frame_botones, text="Anterior", command=self.paso_anterior)
        self.boton_anterior.pack(side=tk.LEFT)
        self.boton_siguiente = tk.Button(frame_botones, text="Siguiente", command=self.paso_siguiente)
        self.boton_siguiente.pack(side=tk.LEFT)
        self.boton_reproducir = tk.Button(frame_botones, text="Reproducir", command=self.reproducir_animacion)
        self.boton_reproducir.pack(side=tk.LEFT)

        self.actualizar_grafo()

    def visitar_dfs(self, nodo):
        self.tiempo += 1
        self.G.nodes[nodo]['descubrimiento'] = self.tiempo
        self.G.nodes[nodo]['color'] = 'gray'
        self.visitados.add(nodo)
        self.pila.append(nodo)
        self.pasos.append(self.G.copy())

        for vecino in self.G.neighbors(nodo):
            if self.G.nodes[vecino]['color'] == 'white':
                self.G.edges[nodo, vecino]['color'] = 'green'
                self.pasos.append(self.G.copy())
                self.visitar_dfs(vecino)

        self.G.nodes[nodo]['color'] = 'black'
        self.tiempo += 1
        self.G.nodes[nodo]['finalización'] = self.tiempo
        self.pila.pop()
        self.pasos.append(self.G.copy())

    def actualizar_grafo(self):
        self.ax.clear()
        colores = [self.G.nodes[nodo]['color'] for nodo in self.G.nodes()]
        
        # Dibujar las aristas
        aristas_recorridas = [(u, v) for (u, v, d) in self.G.edges(data=True) if d.get('color') == 'green']
        aristas_no_recorridas = [(u, v) for (u, v, d) in self.G.edges(data=True) if d.get('color') != 'green']
        
        # Usar self.pos en lugar de calcular un nuevo layout
        nx.draw_networkx_edges(self.G, self.pos, edgelist=aristas_no_recorridas, edge_color='black', ax=self.ax)
        nx.draw_networkx_edges(self.G, self.pos, edgelist=aristas_recorridas, edge_color='red', width=2, ax=self.ax)
        nx.draw_networkx_nodes(self.G, self.pos, node_color=colores, ax=self.ax)
        nx.draw_networkx_labels(self.G, self.pos, ax=self.ax)
        
        if self.pila:
            nx.draw_networkx_nodes(self.G, self.pos, nodelist=[self.pila[-1]], node_color='red', ax=self.ax)
        
        self.canvas.draw()

    def paso_siguiente(self):
        if self.paso_actual < len(self.pasos) - 1:
            self.paso_actual += 1
            self.G = self.pasos[self.paso_actual]
            self.actualizar_grafo()

    def paso_anterior(self):
        if self.paso_actual > 0:
            self.paso_actual -= 1
            self.G = self.pasos[self.paso_actual]
            self.actualizar_grafo()

    def reproducir_animacion(self):
        def animar():
            if self.paso_actual < len(self.pasos) - 1:
                self.paso_siguiente()
                self.root.after(500, animar)  # 500 ms = 0.5 segundos
            else:
                self.boton_reproducir.config(state=tk.NORMAL)

        self.boton_reproducir.config(state=tk.DISABLED)
        animar()

    def ejecutar(self):
        self.root.mainloop()

'''
# Ejemplo de uso
G = nx.Graph()
G.add_edges_from([(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7)])

vis_dfs = VisualizadorDFS(G)
vis_dfs.ejecutar()
'''