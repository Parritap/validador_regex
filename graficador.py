from mermaid.graph import Graph
import mermaid as md
import os

def graficar(graph_instructions : str):

    print("Las instrucciones son ---->: \n" + graph_instructions)
    """ Grafica el grafo y lo guarda en la carpeta resources del proyecto"""
    print("ASEGURESE DE TENER CONEXION A INTERNET")
    print("Renderizando grafo")
    sequence = Graph("Sequence-diagram", graph_instructions)
    render = md.Mermaid(sequence)

    path = "./resources/"
    file = get_path(path, 0)

    render.to_png(file)
    print("grafo renderizado.")


def get_path(path: str, num: int) -> str:
    if os.path.exists(path + str(num) + ".png"):
        return get_path(path, num + 1)
    return path + str(num) + ".png"
