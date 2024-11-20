# Motor de Expresiones Regulares basado en la Construcción de Thompson
Grupo: **[Juan Esteban Parra Parra, Juan Esteban Castaño Osma, Juan Alejandro Gallego]**

Este proyecto implementa un motor de expresiones regulares que utiliza la construcción de 
Thompson para convertir expresiones regulares en autómatas no deterministas finitos (NFA por sus siglas en Inglés).
Una vez convertida la expresión en notación postfix, se construye el NFA, se puede utilizar para verificar si una cadena
dada coincide con la expresión regular.

# Información Básica


### Instalación de paquetes

Usar un entorno virtual de Python "venv"
```bash
python -m venv venv
source venv/bin/activate

#Luego instalamos los paquetes necesarios

pip install mermaid-py
pip install customtkinter
pip install tk


```

### Adiocionalmente en MacOs
```bash
brew install python-tk
```

### O adicionalmente si tiene Ubuntu
```bash
sudo apt install python3-tk
```



### Dependencias
- **re:** Módulo de expresiones regulares de Python, utilizado para la validación de la sintaxis de la expresión regular.

### Características Principales
- **Conversión de expresiones regulares:** Soporta operadores comunes como concatenación, unión, cerradura de Kleene y uno o más.
- **Construcción de autómatas:** Utiliza el algoritmo de Thompson para construir el NFA correspondiente a la expresión regular.
- **Simulación de autómatas:** Simula la ejecución del autómata sobre una cadena de entrada para determinar si es aceptada.
- **Validación de expresiones regulares:** Verifica la sintaxis de la expresión regular antes de procesarla.

### Componentes Principales
- **Nodo:** Representa un estado en un autómata.
- **autómata:** Representa un autómata no determinista que tiene un estado inicial y un estado de aceptación.
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

### autómata
La clase **autómata** representa un un **Autómata No Determinista** (_NFA_).

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


  - _**compilar(self, postfix: str):**_ Esta función compila una expresión regular en notación **postfix** y a partir de ella construye un 
autómata no determinista basado en la construcción de Thompson. 
    - **Funcionamiento:** Esto se realiza a través de la iteración de los caracteres de la expresión, 
que permiten crear autómatas parciales y conectarlos a través de una pila, de la siguiente manera:
      - **'\*' (Cerradura de Kleene):** Se toma el último autómata de la pila y se crea un nuevo autómata donde el estado inicial tiene una transición al estado inicial del autómata original y una transición a un nuevo estado final.
      - **'.' (Concatenación):** Se toman los dos últimos autómatas de la pila. El estado final del primer autómata se conecta al estado inicial del segundo autómata.
      - **'|' (Alternancia):** Se toman los dos últimos autómatas de la pila. Se crea un nuevo estado inicial con transiciones a los estados iniciales de los dos autómatas originales. Se crea un nuevo estado final al que apuntan los estados finales de los dos autómatas originales.
      - **'+' (Uno o más):** Similar a la cerradura de Kleene, pero sin la transición ε del estado final original al estado inicial.
      - **Caracteres:** Se crea un nuevo autómata simple con un estado inicial, un estado final y una transición etiquetada con el carácter.
    - **Parámetros:**
      - _**[String] postfix:**_ La expresión regular ya convertida en notación **postfix.**
    - **Retorno:** Un objeto _automata_ que representa el autómata generado.
    

  - _**seguir_epsilons(self, current_state: Nodo):**_ Esta función encuentra todos los nodos alcanzables desde un nodo inicial
usando solo transiciones epsilon o vacías, esto se hace, ya que un autómata no determinista puede tener este tipo de transiciones 
a otros estados y es necesario determinar todos aquellos que pueden ser alcanzados de esta manera.
    - **Funcionamiento:** Esto se realiza a través de un conjunto de nodos en donde se almacenaran todos los que sean alcanzables con transiciones vacías desde
  el actual que se pide como parametro, a partir del cual se va a iterar verificando que la transición tenga un carácter asignado hasta la _**arista1**_ o _**arista2**_
y al llegar a estas, se agregarán estos nodos vacíos alcanzables de manera recursiva.
    - **Parámetros:**
      - _**[Nodo] current_state:**_ Cualquier nodo en el autómata, a partir del cual se comienza la búsqueda de transiciones epsilon.
    - **Retorno:** Un conjunto de nodos que son alcanzables desde el _**current_state**_ mediante transiciones epsilon.
    

  - _**verificar_str(self, regex: str, texto: str):**_ Esta función verifica si una cadena de texto dada es aceptada por un autómata construido a partir de la expresión regular dada.
La verificación se hace a partir de la simulación de la cadena en el autómata ya previamente construido. Si el autómata llega a un estado de aceptación al final de la cadena, 
    - la función devuelve _**True**_, indicando que el texto es aceptado por la expresión regular. Si no, devuelve _**False.**_
      - **Funcionamiento:** Antes de verificar el string, esta función llama a las demás explicadas en este documento para verificar la
validez de la expresión regular, convertir la expresión a **postfix**, construir el autómata y evaluar los estados a los que puede llegar
con transiciones vacías. 
    
      &emsp; Una vez realizado esto se recorre cada carácter del texto y por cada uno de estos se crea un conjunto de estados siguientes,
si hay una transición que coincida con el carácter, el estado se agrega al conjunto anterior y se actualiza el nodo del set _**current**_ con los nuevos estados alcanzables.
Para que la cadena sea válida al procesar el último carácter se debe de llegar a un estado de aceptación en el autómata.
    - **Parámetros:**
      - _**[String] regex:**_ La expresión regular en notación **infija** usada normalmente para escribirlas.
      - _**[String] texto:**_ La cadena cuya aceptación se desea verificar a partir de _**regex.**_
    - **Retorno:** Un booleano, _**True**_ si la cadena es aceptada por el autómata generado a partir de la expresión regular, o _**False**_ en el caso contrario.  
    

  - _**verificar_validez_regex(self, regex: str):**_ Esta función verifica la sintaxis de una expresión regular, asegurándose que cumplan con una serie
de reglas estructurales en el contexto de este motor. Verificando caracteres, ubicaciones o secuencias no permitidas.
    - **Funcionamiento:**
      - Verifica caracteres no permitidos a partir de la expresión regular `^[a-zA-Z0-9+\|\(\)\.\*]+$` permitiendo solo 
letras mayúsculas, minúsculas, números, paréntesis y los operadores permitidos.
      - Verifica que no se comience con un operador a partir de la expresión regular `^[+\|\.\*]`.
      - Verifica que no estén dos operadores consecutivos a partir de la expresión regular `[+\|\.\*]{2,}`.
      - Verifica que los operadores _+_ y _\*_ no los suceda un carácter no válido a partir de la expresión regular `[+\*][^a-zA-Z0-9\)]`.
      - Verifica que los operadores _|_ y _._ no estén rodeados incorrectamente a partir de la expresión regular `[\|\.][^a-zA-Z0-9()\.]|[^a-zA-Z0-9()\.][\|\.]`.
    - **Parámetros:**
      - _**[String] regex:**_ La expresión regular que se desea validar.
    - **Retorno:** Un booleano, _**True**_ si se pasan todas las validaciones o _**False**_ en caso de que al menos una no pueda pasar.

## Ejemplo de uso [Consola]
Este proyecto cuenta con interfaz gráfica, sin embargo, por términos de practicidad, se mostrará el ejemplo de su funcionamiento en consola,
puesto que la forma de interactuar con el programa es prácticamente la misma en ambos casos. 
```
Ingrese el regex (o 'salir' o 'q' para salir): a.(b|d).c*
Ingrese el texto a validar: abcc
Resultado del match: True
```
