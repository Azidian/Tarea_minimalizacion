from collections import defaultdict, deque # Importa estructuras útiles: defaultdict crea listas automáticas, deque es una cola eficiente

def readints(s: str):
    s = s.strip() # Elimina espacios en blanco al inicio y fin de la cadena
    return list(map(int, s.split())) if s else [] # Convierte la cadena en lista de enteros, si no está vacía; si está vacía devuelve []

def parse_transitions(lines, n, k):
    trans = []  # Aquí se guardarán las transiciones del autómata
    i = 0 # Índice para recorrer las líneas
    while len(trans) < n: # Necesitamos n filas de transiciones
        if i >= len(lines):  # Si no hay suficientes líneas
            raise ValueError("Faltan filas de transiciones.") # Muestra error en pantalla al usuario
        row = lines[i].strip() # Tomamos la línea actual sin espacios extra
        i += 1
        if row == "":# Si está vacía, la saltamos
            continue
        nums = readints(row)  # Convertimos la línea en lista de enteros
        if len(nums) == k:  # Si hay k números, corresponde a las transiciones correctas
            trans.append(nums)
        elif len(nums) == k + 1: # Si hay k+1 números, ignoramos el primero (normalmente el estado) y tomamos los últimos k
            trans.append(nums[-k:])
        else:
            raise ValueError(
                f"Fila de transiciones con {len(nums)} números; se esperaban {k} o {k+1}: '{row}'"
            )
    return trans, i # Devuelve la tabla de transiciones y cuántas líneas se consumieron

def kozen_equivalences(n, k, trans, finals):
    parents = defaultdict(list) # Diccionario que guarda qué pares dependen de otros pares
    pairs = [] # Lista de todos los pares de estados posibles (p,q) con p<q
    for p in range(n):  # Recorremos los estados
        for q in range(p + 1, n): # Solo pares distintos, evitando duplicados
            pairs.append((p, q))  # Guardamos el par
            for ai in range(k):
                r, s = trans[p][ai], trans[q][ai] # A dónde va p y q con ese símbolo
                if r != s: # Si transitan a estados distintos 
                    a, b = (r, s) if r < s else (s, r) # Ordenamos (a,b) para consistencia
                    parents[(a, b)].append((p, q)) # Decimos: el par (p,q) depende de (a,b)

    marked = set()
    dq = deque()  # Cola para propagar los pares 

    for p, q in pairs: # Recorremos todos los pares
        if (p in finals) ^ (q in finals):
            marked.add((p, q))  # Son distinguibles
            dq.append((p, q))  # Los metemos a la cola 


    while dq: # Mientras haya pares distinguidos en la cola
        r, s = dq.popleft() # Sacamos un par
        for p, q in parents.get((r, s), ()): # Vemos qué pares dependen de él
            if (p, q) not in marked: # Si aún no estaban distinguidos
                marked.add((p, q)) # Los marcamos
                dq.append((p, q)) # Y los añadimos a la cola para seguir propagando

    equiv = [pair for pair in pairs if pair not in marked] # Los pares que NO fueron marcados son equivalentes
    equiv.sort()  # Funcion de ordenamiento, para mostrar de forma limpia
    return " ".join(f"({p},{q})" for p, q in equiv) # Devolvemos como texto "(p,q)" 

def main():
    with open("ejemplo.txt", "r", encoding="utf-8") as f: # Abrimos el archivo de entrada
        data = f.read().splitlines()  # Leemos todas las líneas en una lista

    idx = 0 # Índice para recorrer líneas
    while idx < len(data) and data[idx].strip() == "":# Saltamos líneas vacías al inicio
        idx += 1
    if idx >= len(data):
        return
    c = int(data[idx].strip()); idx += 1 # Número de casos de prueba

    out_lines = []  # Aquí se guardan los resultados

    for _ in range(c):  # Para cada caso
        while idx < len(data) and data[idx].strip() == "":
            idx += 1
        n = int(data[idx].strip()); idx += 1

        while idx < len(data) and data[idx].strip() == "":
            idx += 1
        alphabet = data[idx].strip().split(); idx += 1  # Leemos el alfabeto
        k = len(alphabet) # Tamaño del alfabeto
        if k == 0: 
            raise ValueError("Línea de alfabeto vacía.")  # Si el alfabeto esta vacío muestra un error en la pantalla del usuario 

        finals_line = data[idx] if idx < len(data) else "" # Línea con estados finales
        idx += 1
        finals = set(readints(finals_line)) # Convertimos en conjunto

        trans, consumed = parse_transitions(data[idx:], n, k) # Construye la tabla de transiciones del autómata a partir de las siguientes líneas del archivo
        idx += consumed # Avanzamos el índice

        out_lines.append(kozen_equivalences(n, k, trans, finals)) # Calculamos equivalencias y guardamos

    print("\n".join(out_lines)) # Mostramos todos los resultados

if __name__ == "__main__": # Punto de entrada
    main() # Ejecuta el programa principal
