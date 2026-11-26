from collections import deque
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np




class GraficaMetro:


    def __init__(self):
        self.adyacencia = {}
        self.coordenadas = {}


    def agregar_estacion(self, nombre, x, y):
        if nombre not in self.adyacencia:
            self.adyacencia[nombre] = []
            self.coordenadas[nombre] = (x, y)


    def agregar_tramo(self, u, v):
        if u in self.adyacencia and v in self.adyacencia:
            if v not in self.adyacencia[u]:
                self.adyacencia[u].append(v)
            if u not in self.adyacencia[v]:
                self.adyacencia[v].append(u)


    def obtener_matriz_adyacencia(self):
        nodos = sorted(self.adyacencia.keys())
        n = len(nodos)
        indice = {nodo: i for i, nodo in enumerate(nodos)}
        matriz = np.zeros((n, n), dtype=int)


        for u in nodos:
            for v in self.adyacencia[u]:
                matriz[indice[u]][indice[v]] = 1
        return nodos, matriz


    def bfs_ruta_minima(self, inicio, destino, estaciones_cerradas=None):
        if estaciones_cerradas is None:
            estaciones_cerradas = set()


        if inicio in estaciones_cerradas or destino in estaciones_cerradas:
            return None, [], []


        visitados = set([inicio])
        cola = deque([[inicio]])
        aristas_arbol_bfs = []
        orden_exploracion = []


        while cola:
            camino = cola.popleft()
            actual = camino[-1]
            orden_exploracion.append(actual)


            if actual == destino:
                return camino, aristas_arbol_bfs, orden_exploracion


            for vecino in self.adyacencia[actual]:
                if (
                    vecino not in visitados
                    and vecino not in estaciones_cerradas
                ):
                    visitados.add(vecino)
                    aristas_arbol_bfs.append((actual, vecino))
                    nuevo_camino = list(camino)
                    nuevo_camino.append(vecino)
                    cola.append(nuevo_camino)


        return None, aristas_arbol_bfs, orden_exploracion


    def _dfs_recursivo(self, nodo, visitados, componente, estaciones_cerradas):
        visitados.add(nodo)
        componente.append(nodo)
        for vecino in self.adyacencia[nodo]:
            if vecino not in visitados and vecino not in estaciones_cerradas:
                self._dfs_recursivo(
                    vecino, visitados, componente, estaciones_cerradas
                )


    def obtener_componentes_conexas(self, estaciones_cerradas=None):
        if estaciones_cerradas is None:
            estaciones_cerradas = set()


        visitados = set()
        componentes = []


        for estacion in self.adyacencia:
            if (
                estacion not in visitados
                and estacion not in estaciones_cerradas
            ):
                componente_actual = []
                self._dfs_recursivo(
                    estacion, visitados, componente_actual, estaciones_cerradas
                )
                componentes.append(componente_actual)


        return componentes


    def detectar_puntos_articulacion(self):
        componentes_base = len(self.obtener_componentes_conexas())
        puntos_criticos = []


        for estacion in sorted(self.adyacencia.keys()):
            componentes_sin_estacion = len(
                self.obtener_componentes_conexas({estacion})
            )
            if componentes_sin_estacion > componentes_base:
                puntos_criticos.append((estacion, componentes_sin_estacion))


        return puntos_criticos




def construir_red_metro():
    metro = GraficaMetro()


    estaciones = [
        ("Universidad", 0, 0),
        ("Copilco", 0, 1),
        ("M.A. Quevedo", 0, 2),
        ("Zapata", 0, 3),
        ("Centro Médico", 0, 5),
        ("Balderas", 0, 7),
        ("Hidalgo", 0, 8),
        ("Guerrero", 0, 9),
        ("Tacubaya", -3, 5),
        ("Mixcoac", -3, 3),
        ("Insurgentes", -1.5, 6.5),
        ("Pino Suárez", 1.5, 7),
        ("Chabacano", 1.5, 5),
        ("Ermita", 1.5, 3),
        ("Tasqueña", 1.5, 1),
        ("Bellas Artes", 0.8, 8),
        ("Garibaldi", 0.8, 9),
        ("Pantitlán", 4, 6),
        ("Jamaica", 2.5, 5),
    ]


    for nombre, x, y in estaciones:
        metro.agregar_estacion(nombre, x, y)


    tramos = [
        ("Universidad", "Copilco"),
        ("Copilco", "M.A. Quevedo"),
        ("M.A. Quevedo", "Zapata"),
        ("Zapata", "Centro Médico"),
        ("Centro Médico", "Balderas"),
        ("Balderas", "Hidalgo"),
        ("Hidalgo", "Guerrero"),
        ("Tacubaya", "Insurgentes"),
        ("Insurgentes", "Balderas"),
        ("Balderas", "Pino Suárez"),
        ("Pino Suárez", "Pantitlán"),
        ("Hidalgo", "Bellas Artes"),
        ("Bellas Artes", "Pino Suárez"),
        ("Pino Suárez", "Chabacano"),
        ("Chabacano", "Ermita"),
        ("Ermita", "Tasqueña"),
        ("Tacubaya", "Centro Médico"),
        ("Centro Médico", "Chabacano"),
        ("Chabacano", "Jamaica"),
        ("Jamaica", "Pantitlán"),
        ("Tacubaya", "Mixcoac"),
        ("Mixcoac", "Zapata"),
        ("Zapata", "Ermita"),
        ("Guerrero", "Garibaldi"),
        ("Garibaldi", "Bellas Artes"),
    ]


    for u, v in tramos:
        metro.agregar_tramo(u, v)


    return metro




def visualizar_resultados(metro, ruta_bfs, estacion_falla, componentes_falla):
    G = nx.Graph()
    for u, vecinos in metro.adyacencia.items():
        for v in vecinos:
            G.add_edge(u, v)


    pos = metro.coordenadas
    fig, axes = plt.subplots(1, 2, figsize=(16, 7))


    ax1 = axes[0]
    ax1.set_title(
        "1. Búsqueda en Anchura (BFS)\nRuta mínima: Universidad -> Pantitlán",
        fontsize=11,
        fontweight="bold",
    )


    aristas_ruta = (
        list(zip(ruta_bfs[:-1], ruta_bfs[1:])) if ruta_bfs else []
    )
    colores_nodos_1 = [
        "#ff5722" if n in ruta_bfs else "#90caf9" for n in G.nodes()
    ]
    colores_aristas_1 = [
        "#d32f2f"
        if (u, v) in aristas_ruta or (v, u) in aristas_ruta
        else "#b0bec5"
        for u, v in G.edges()
    ]
    anchos_aristas_1 = [
        3.5 if (u, v) in aristas_ruta or (v, u) in aristas_ruta else 1.2
        for u, v in G.edges()
    ]


    nx.draw(
        G,
        pos,
        ax=ax1,
        with_labels=True,
        node_color=colores_nodos_1,
        edge_color=colores_aristas_1,
        width=anchos_aristas_1,
        node_size=550,
        font_size=7.5,
        font_weight="bold",
    )


    ax2 = axes[1]
    ax2.set_title(
        f"2. Búsqueda en Profundidad (DFS)\nFalla simulada en '{estacion_falla}' ({len(componentes_falla)} componentes conexas)",
        fontsize=11,
        fontweight="bold",
    )


    paleta = ["#66bb6a", "#ffa726", "#ab47bc", "#29b6f6"]
    mapa_colores = {}
    for idx, comp in enumerate(componentes_falla):
        for nodo in comp:
            mapa_colores[nodo] = paleta[idx % len(paleta)]
    mapa_colores[estacion_falla] = "#212121"


    colores_nodos_2 = [mapa_colores[n] for n in G.nodes()]
    colores_aristas_2 = [
        "#eeeeee" if estacion_falla in (u, v) else "#78909c"
        for u, v in G.edges()
    ]


    nx.draw(
        G,
        pos,
        ax=ax2,
        with_labels=True,
        node_color=colores_nodos_2,
        edge_color=colores_aristas_2,
        width=1.5,
        node_size=550,
        font_size=7.5,
        font_weight="bold",
    )


    plt.tight_layout()
    plt.show()




if __name__ == "__main__":
    metro = construir_red_metro()


    print("=" * 65)
    print("ANÁLISIS DE TEORÍA DE GRÁFICAS - RED METRO CDMX")
    print("=" * 65)


    nodos, matriz = metro.obtener_matriz_adyacencia()
    print(f"\n[1] Orden de la gráfica |V| = {len(nodos)} estaciones.")
    print("Submatriz de adyacencia (primeras 8 estaciones alfabéticamente):")
    print("   ", " ".join([n[:4] for n in nodos[:8]]))
    for i in range(8):
        fila = "   ".join(map(str, matriz[i, :8]))
        print(f"{nodos[i][:4]:<4} {fila}")


    origen, destino = "Universidad", "Pantitlán"                                                #########
    ruta, arbol_bfs, explorados = metro.bfs_ruta_minima(origen, destino)
    print(f"\n[2] Algoritmo BFS ({origen} -> {destino}):")
    print(
        f"    -> Ruta óptima ({len(ruta)-1} tramos): {' -> '.join(ruta)}"
    )
    print(f"    -> Nodos explorados antes de hallar destino: {len(explorados)}")


    criticos = metro.detectar_puntos_articulacion()
    print("\n[3] Algoritmo DFS - Puntos de Articulación (Estaciones Críticas):")
    if criticos:
        for est, num_comp in criticos:
            print(
                f"    -> Al cerrar '{est}', la red se fragmenta en {num_comp} componentes conexas."
            )
    else:
        print("    -> La red es 2-conexa (ningún nodo individual la desconecta).")


    estacion_prueba = "Centro Médico","Tacubaya"  if criticos else "Centro Médico"                               ##########
    componentes_tras_falla = metro.obtener_componentes_conexas({estacion_prueba})
    print(f"\n[4] Componentes resultantes al cerrar '{estacion_prueba}':")
    for idx, comp in enumerate(componentes_tras_falla, 1):
        print(f"    Componente {idx} ({len(comp)} estaciones): {comp}")


    visualizar_resultados(metro, ruta, estacion_prueba, componentes_tras_falla)
