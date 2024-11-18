# Motor de Expresiones Regulares basado en la Construcción de Thompson
Grupo: **[Juan Esteban Parra Parra, Juan Esteban Castaño Osma, Juan Alejandro Gallego ]**

Este proyecto implementa un motor de expresiones regulares que utiliza la construcción de 
Thompson para convertir expresiones regulares en autómatas no deterministas finitos (NFA por sus siglas en Inglés).
Una vez convertida la expresión en notación postfix, se construye el NFA, se puede utilizar para verificar si una cadena
dada coincide con la expresión regular.

### Instalación

No se requiere instalación específica.  Asegúrese de tener Python 3 instalado.

### Caracteristicas Principales
- **Conversión de expresiones regulares:** Soporta operadores comunes como concatenación, unión, cerradura de Kleene y uno o más.
- **Construcción de autómatas:** Utiliza el algoritmo de Thompson para construir el NFA correspondiente a la expresión regular.
- **Simulación de autómatas:** Simula la ejecución del autómata sobre una cadena de entrada para determinar si es aceptada.
- **Validación de expresiones regulares:** Verifica la sintaxis de la expresión regular antes de procesarla.

### Componentes Principales
- **Nodo:** Representa un estado en un autómata.
- **Automata:** Representa un autómata no determinista que tiene un estado inicial y un estado de aceptación.
- **MotorRegex:** Implementa la lógica para convertir una expresión regular en un autómata no determinista y verificar la validez de una cadena.

## Clases

### Nodo
La clase **Nodo** representa un estado dentro de un **Autómata No Determinista**.

- **Atributos:**
  - _**[String] etiqueta:**_ Es un carácter, excepto en los estados de aceptación y transición epsilon, donde puede ser _None_.
  - _**[Nodo] arista1 y arista2:**_ Son punteros a otros nodos, los cuales representan las transiciones del autómata. Un nodo puede tener hasta dos aristas a otros nodos.
  
- **Métodos:**
  - _**\_\_hash\_\_:**_ Esta función devuelve el valor del hash para el nodo, se usa cuando se quiere agregar un nodo a un set.
  - _**\_\_eq\_\_:**_ Esta función Compara dos nodos para verificar si son iguales basados en su etiqueta y conexiones de aristas.

### Automata
La clase **Automata** representa un un **Autómata No Determinista** (_NFA_).

- **Atributos:**
  - _**[Nodo] inicial:**_ Nodo inicial del autómata.
  - _**[Nodo] aceptacion:**_ Nodo final o nodo de aceptación del autómata.

### Motor Regex
La clase **Motor Regex** se encarga de compilar la expresión regular y de verificar la validez de una cadena a través de
un **Autómata No Determinista** el cual es resultado de la compilación mencionada anteriormente

- **Atributos:**
  - _**[Diccionario - Char] operadores:**_ Diccionario que contiene los operadores de las expresiones regulares con su respectivo nivel de precedencia.
  - _**[Arreglo - Char] postfix:**_ Arreglo que almacena la expresión regular en notación **postfix** (_Notación polaca inversa_).

- **Métodos:**
  - _**infix_a_postfix(self, infix: str):**_ Esta función convierte una expresión regular en notación **infix** a notación **postfix.** Este proceso es necesario para 
simplificar el proceso de construcción del autómata. 
    - **Funcionamiento:** Esto se realiza almacenando la expresión en una pila, eliminando los carácteres de agrupación y finalmente almacenando 
los restantes mediante la funcionalidad de la pila la cual siempre retorna el último objeto almacenado en la misma.
    - **Parámetros:**
      - _**infix:**_ Expresión regular en notación **infix**, esta es la expresión regular solicitada al usuario.
    - **Retorno:** Expresión regular en notación **postfix.**

  - _**compilar(self, postfix: str):**_ Esta función Compila una expresión regular en notación **postfix** y a partir de ella construye un 
autómata no determinista basado en la construcción de Thompson. 
    - **Funcionamiento:** Esto se realiza a través de la iteración de los caracteres de la expresión, 
que permiten crear automatas parciales y conectarlos a través de una pila, de la siguiente manera:
      - **'\*' (Cerradura de Kleene):** Se toma el último autómata de la pila y se crea un nuevo autómata donde el estado inicial tiene una transición al estado inicial del autómata original y una transición a un nuevo estado final.
      - **'.' (Concatenación):** Se toman los dos últimos autómatas de la pila. El estado final del primer autómata se conecta al estado inicial del segundo autómata.
      - **'|' (Alternancia):** Se toman los dos últimos autómatas de la pila. Se crea un nuevo estado inicial con transiciones a los estados iniciales de los dos autómatas originales. Se crea un nuevo estado final al que apuntan los estados finales de los dos autómatas originales.
      - **'+' (Uno o más):** Similar a la cerradura de Kleene, pero sin la transición ε del estado final original al estado inicial.
      - **Caracteres:** Se crea un nuevo autómata simple con un estado inicial, un estado final y una transición etiquetada con el carácter.
    - **Parámetros:**
      - _**[String] postfix:**_ La expresión regular ya convertida en notación **postfix.**
    - **Retorno:** Un objeto _Automata_ que representa el autómata generado.
## Estado -> NO TERMINADO. 
