#!/usr/bin/python3
import re
from dataclasses import dataclass
from typing import Optional, Set
import string
import graficador


# Lambda symbol ---> λ


@dataclass
class Nodo:
    symbolx: str = None # Char que se va a renderizar. No debe ser usado como etiqueta.

    """Nodo representa un estado de un automata."""
    etiqueta: Optional[str] = None
    # Según este articulo -> https://en.wikipedia.org/wiki/Thompson%27s_construction#:~:text=In%20computer%20science%2C%20Thompson
    # Podemos representar un automata no determinista mediante más automatas no deterministas de manera recursiva.
    # Para ello lo unico que necesitamos es que cada nodo contenga máximo dos aristas.
    arista1: Optional["Nodo"] = None
    arista2: Optional["Nodo"] = None

    # Métodos necesarios para poder hashear y comparar nodos.
    # Esto es importante para poder agregar nodos a un set.
    def __hash__(self):
        return hash((self.etiqueta, id(self.arista1), id(self.arista2)))

    def __eq__(self, other):
        if not isinstance(other, Nodo):
            return NotImplemented
        return (self.etiqueta, id(self.arista1), id(self.arista2)) == (
            other.etiqueta,
            id(other.arista1),
            id(other.arista2),
        )


class Renderex:
    """Clase que contiene una logica auxiliar para ayudar a Mermaid a renderizar un diagrama de estados."""

    script: str
    letters: dict = {}

    def __init__(self):
        self.script = "stateDiagram-v2\n"
        self.letters["λ"] = 0
        # Fill the map with the letters of the alphabets
        self.letters.update({letter: 0 for letter in string.ascii_lowercase})

    def get_symbolx(self, c: str) -> str:
        """Logica necesaria dada la manera en como funciona Mermaid"""
        reps = self.letters[c]
        self.letters[c] += 1
        return c + "\0" * reps

    def get_void_node(self) -> Nodo:
        """Retorna un nodo vacío con un 'λ' como symbolx."""
        return Nodo(symbolx=self.get_symbolx("λ"))

    def write(self, instruction: str) -> None:
        """Escribe una instrucción en el script para el algoritmo de Mermaid"""
        self.script += '\t' + instruction + "\n"


@dataclass
class Automata:
    """Automata representa un automata no determinista."""

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
        self.automata = None
        self.operadores = {
            "*": 3,  # Kleene star
            "+": 3,  # One or more
            ".": 2,  # Concatenation
            "|": 1,  # Alternation
        }
        self.postfix = None  # Inicializamos la variable de clase
        self.r = Renderex()  # Renderizador.

    def infix_a_postfix(self, infix: str) -> str:
        """Convierte una expresion regular en notacion infix a postfix (notación polaca inversa).
        La notación infix es la que todos conocemos y usamos en clase.
        Esto es importante porque la notacion postfix resulta más facilmente procesable por una computadora,
        y a la larga, hace menos complejos los algoritmos de analisis de expresiones.

        Ejemplo:
        intput: a.(b|d).c*
        output: abd|.c*.

        https://en.wikipedia.org/wiki/Reverse_Polish_notation#:~:text=9%20External%20links-,Explanation,5%20is%20added%20to%20it.

        """
        postfix = []
        pila = []

        for char in infix:
            if char == "(":
                pila.append(char)
            elif char == ")":
                while pila and pila[-1] != "(":
                    postfix.append(pila.pop())
                if pila:  # Elimina el caracter de agrupacion -> '('
                    pila.pop()
            elif char in self.operadores:
                while (
                    pila
                    and pila[-1] != "("
                    and self.operadores.get(char, 0) <= self.operadores.get(pila[-1], 0)
                ):
                    postfix.append(pila.pop())
                pila.append(char)
            else:
                postfix.append(char)

        # Al terminar el ciclo 'for', solo quedan operadores en la pila.
        # El último paso es agregarlos a la expresion postfix.
        while pila:
            postfix.append(pila.pop())

        resultado = "".join(postfix)
        return resultado

    def compilar(self, postfix: str) -> Automata:
        print(f"La expresion regular en notacion postfix es: {postfix}")
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
                if char == "*":
                    auto1 = auto_stack.pop()
                    init, final = Nodo(), Nodo()
                    init.arista1 = auto1.inicial
                    init.arista2 = final
                    auto1.aceptacion.arista1 = auto1.inicial
                    auto1.aceptacion.arista2 = final
                    auto_stack.append(Automata(init, final))
                elif char == ".":
                    auto2, auto1 = auto_stack.pop(), auto_stack.pop()
                    auto1.aceptacion.arista1 = auto2.inicial
                    auto_stack.append(Automata(auto1.inicial, auto2.aceptacion))
                elif char == "|":
                    auto2, auto1 = auto_stack.pop(), auto_stack.pop()
                    init = Nodo(arista1=auto1.inicial, arista2=auto2.inicial)
                    final = Nodo()
                    auto1.aceptacion.arista1 = final
                    auto2.aceptacion.arista1 = final
                    auto_stack.append(Automata(init, final))
                elif char == "+":
                    auto1 = auto_stack.pop()
                    init, final = Nodo(), Nodo()
                    init.arista1 = auto1.inicial
                    auto1.aceptacion.arista1 = auto1.inicial
                    auto1.aceptacion.arista2 = final
                    auto_stack.append(Automata(init, final))
            else:  # es un caracter
                final = Nodo()
                init = Nodo(etiqueta=char, arista1=final)
                auto_stack.append(Automata(init, final))


        result = auto_stack.pop()
        self.automata = result
        return result


    def fill_symbols (self, nodo : Nodo) -> str :
        if (nodo.symbolx == None) :
            if (nodo.etiqueta == None) :
                nodo.symbolx = self.r.get_symbolx("λ")
            else: nodo.symbolx = self.r.get_symbolx(nodo.etiqueta)

        if (nodo.arista1 != None) :
            self.r.write(f"{nodo.symbolx} --> {self.fill_symbols(nodo.arista1)}")
        if (nodo.arista2 != None) :
            self.r.write(f"{nodo.symbolx} --> {self.fill_symbols(nodo.arista2)}")

        return nodo.symbolx

    def seguir_epsilons(self, current_state: Nodo) -> Set[Nodo]:
        """Obtiene todos los nodos no-epsilon alcanzables siguiendo un camino de nodos epsilon."""
        states = set()
        states.add(current_state)

        if current_state.etiqueta is None:
            if current_state.arista1:
                states |= self.seguir_epsilons(current_state.arista1)
            if current_state.arista2:
                states |= self.seguir_epsilons(current_state.arista2)

        return states

    def verificar_str(self, regex: str, texto: str) -> bool:
        if self.verificar_validez_regex(regex):
            """Con base al regex especificado crea un automata y con base al autómata valida el texto."""
            self.postfix: string = self.infix_a_postfix(regex)
            automata = self.compilar(self.postfix)

            current : set = self.seguir_epsilons(automata.inicial)

            for char in texto:
                next_states = set()
                for state in current:
                    if state.etiqueta == char:
                        next_states |= self.seguir_epsilons(state.arista1)
                current = next_states

            return automata.aceptacion in current
        else:
            return None

    def verificar_validez_regex(self, regex: str) -> bool:
        # Patrón para caracteres alfanuméricos o símbolos permitidos
        patron_caracteres = r"^[a-zA-Z0-9+\|\(\)\.\*]+$"

        # Patrones para verificar secuencias no permitidas
        patron_dos_simbolos = r"[+\|\.\*]{2,}"
        patron_simbolo_al_inicio = r"^[+\|\.\*]"
        patron_simbolo_sin_alfanumerico_derecha = r"[+\*][^a-zA-Z0-9\)]"
        patron_simbolo_sin_alfanumerico_ambos_lados = (
            r"[\|\.][^a-zA-Z0-9()\.]|[^a-zA-Z0-9()\.][\|\.]"
        )

        # Verificar si la expresión contiene al menos un caracter alfanumérico o símbolo permitido
        if not re.search(patron_caracteres, regex):
            print("1 NO VALIDA")
            return False

        # Verificar si la expresión comienza con un caracter alfanumérico
        if re.match(patron_simbolo_al_inicio, regex):
            print("2 NO VALIDA")
            return False

        # Verificar si hay dos o más símbolos consecutivos
        if re.search(patron_dos_simbolos, regex):
            print("3 NO VALIDA")
            return False

        # Verificar si hay símbolos "+" o "*" sin un caracter alfanumérico o ")" a la izquierda
        if re.search(patron_simbolo_sin_alfanumerico_derecha, regex):
            print("4 NO VALIDA")
            return False

        # Verificar si hay símbolos "." o "|" sin un caracter alfanumérico o ")" a ambos lados
        if re.search(patron_simbolo_sin_alfanumerico_ambos_lados, regex):
            print("5 NO VALIDA")
            return False

        return True


def main():
    """Ejemplo de uso de la clase MotorRegex."""
    motor = MotorRegex()

    while True:
        try:
            user_input = input("Ingrese el regex (o 'salir' o 'q' para salir): ")
            if user_input.lower() in ("salir", "q"):
                break
            texto = input("Ingrese el texto a validar: ")
            matches = motor.verificar_str(user_input, texto)

            if matches is None:
                print("ERROR")
            else:
                print(f"\nResultado del match: {matches}\n")

            #Procesamos cada nodo para obtener la lista de instrucciones de Mermaid
            motor.fill_symbols(motor.automata.inicial)
            # Graficamos el automata
            graficador.graficar(motor.r.script)


        except KeyboardInterrupt:
            break



if __name__ == "__main__":
    main()
