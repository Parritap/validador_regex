from dataclasses import dataclass
from typing import Optional, Set
import string


@dataclass
class Nodo:
    """Nodo representa un estado de un automata."""
    # Es de tipo Optional dado que el valor None equivale a un epsilon.}
    # La etiqueta representa la transación que se debe realizar para llegar a este nodo, es por esto que
    # vemos que cada nodo contiene una sola etiqueta o peso.
    etiqueta: Optional[str] = None
    # Según este articulo -> https://en.wikipedia.org/wiki/Thompson%27s_construction#:~:text=In%20computer%20science%2C%20Thompson
    # Podemos representar un automata no determinasta mediante más automatas no deterministas de manera recursiva.
    # Para ello lo unico que necesitamos es que cada nodo contenga máximo dos aristas.
    arista1: Optional['Nodo'] = None
    arista2: Optional['Nodo'] = None

    # Métodos necesarios para poder hashear y comparar nodos.
    # Esto es importante para poder agregar nodos a un set.
    def __hash__(self):
        return hash((self.etiqueta, id(self.arista1), id(self.arista2)))

    def __eq__(self, other):
        if not isinstance(other, Nodo):
            return NotImplemented
        return (self.etiqueta, id(self.arista1), id(self.arista2)) == (
            other.etiqueta, id(other.arista1), id(other.arista2))


@dataclass
class Automata:
    """ Automata representa un automata no determinista."""
    inicial: Nodo
    aceptacion: Nodo


class MotorRegex:
    """Clase que funciona con base a un expresion regular dada,
    la cual se compila en un automata no determinista que podrá
    verificar la validez de una cadena de texto dada.
    """

    """
    El siguiente es un diccionario que contiene los operadores con su respectivo nivel de precedencia.
    El nivel de precedencia es simplemente el nivel de jerarquia que tiene un operador sobre otro.
    
    Haciendo un ejemplo en un contexto más conocido: En el algebra el operador de multiplicación tiene mayor
    precedencia que el operador de suma, esto quiere decir que en la siguiente expresion : A + B * C
    Primero se realizará la multiplicación y luego la suma.
    
    En las expresiones regulares ocurre lo mismo.
    """

    def __init__(self):
        self.operadores = {
            '*': 3,  # Kleene star
            '+': 3,  # One or more
            '.': 2,  # Concatenation
            '|': 1  # Alternation
        }




    def infix_a_postfix(self, infix: str) -> str:
        """Convierte una expresion regular en notacion infix a postfix (notación polaca inversa).
        La notación infix es la que todos conocemos y usamos en clase.
        Esto es importante porque la notacion postfix resulta más facilmente procesable por una computadora,
        y a la larga, hace menos complejos los algoritmos de analisis de expresiones.

        Ejemplo -> a.(b|d).c*  ------> abd|.c*.

        https://en.wikipedia.org/wiki/Reverse_Polish_notation#:~:text=9%20External%20links-,Explanation,5%20is%20added%20to%20it.

        """
        postfix = []
        pila = []

        for char in infix:
            if char == '(':
                pila.append(char)
            elif char == ')':
                while pila and pila[-1] != '(':
                    postfix.append(pila.pop())
                if pila:  # Elimina el caracter de agrupacion -> '('
                    pila.pop()
            elif char in self.operadores:
                while (pila and pila[-1] != '(' and
                       self.operadores.get(char, 0) <= self.operadores.get(pila[-1], 0)):
                    postfix.append(pila.pop())
                pila.append(char)
            else:
                postfix.append(char)

        # Al terminar el ciclo 'for', solo quedan operadores en la pila.
        # El último paso es agregarlos a la expresion postfix.
        while pila:
            postfix.append(pila.pop())

        resultado = ''.join(postfix)
        print(f"La expresion regular en notacion postfix es: {resultado}")
        return resultado

    def compilar(self, postfix: str) -> Automata:
        """Se encarga de contruir un automata no determinista con base a la expresion postfix
        Este algoritmo se ve complejo pero basta con dibujar el proceso que sigue para ver
        que simplemente crea, arma y desarma autoamatas, conectando unos con otros de cierta manera dependiendo del
        operador.

        Para mayor claridad del algoritmo, ver la siguiente imagen que representa el regex : (ε|a*b)
        https://en.wikipedia.org/wiki/Thompson%27s_construction#/media/File:Small-thompson-example.svg
        """
        auto_stack = []  # Pila del automata

        for char in postfix:
            if char in self.operadores:
                if char == '*':
                    auto1 = auto_stack.pop()
                    inicial, aceptacion = Nodo(), Nodo()
                    inicial.arista1 = auto1.inicial
                    inicial.arista2 = aceptacion
                    auto1.aceptacion.arista1 = auto1.inicial
                    auto1.aceptacion.arista2 = aceptacion
                    auto_stack.append(Automata(inicial, aceptacion))
                elif char == '.':
                    auto2, auto1 = auto_stack.pop(), auto_stack.pop()
                    auto1.aceptacion.arista1 = auto2.inicial
                    auto_stack.append(Automata(auto1.inicial, auto2.aceptacion))
                elif char == '|':
                    auto2, auto1 = auto_stack.pop(), auto_stack.pop()
                    inicial = Nodo(arista1=auto1.inicial, arista2=auto2.inicial)
                    aceptacion = Nodo()
                    auto1.aceptacion.arista1 = aceptacion
                    auto2.aceptacion.arista1 = aceptacion
                    auto_stack.append(Automata(inicial, aceptacion))
                elif char == '+':
                    auto1 = auto_stack.pop()
                    inicial, aceptacion = Nodo(), Nodo()
                    inicial.arista1 = auto1.inicial
                    auto1.aceptacion.arista1 = auto1.inicial
                    auto1.aceptacion.arista2 = aceptacion
                    auto_stack.append(Automata(inicial, aceptacion))
                elif char == '?':
                    auto1 = auto_stack.pop()
                    inicial, aceptacion = Nodo(), Nodo()
                    inicial.arista1 = auto1.inicial
                    inicial.arista2 = aceptacion
                    auto1.aceptacion.arista1 = aceptacion
                    auto_stack.append(Automata(inicial, aceptacion))
            else:
                aceptacion = Nodo()
                inicial = Nodo(etiqueta=char, arista1=aceptacion)
                auto_stack.append(Automata(inicial, aceptacion))

        return auto_stack.pop()
