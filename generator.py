import random

# Función para determinar el tipo de instancia y generar número de salas y asignaturas
def num_salas_asig(tipo_instancia):
    if tipo_instancia == 'Medianas':
        num_salas = random.randint(3, 7)
        num_asignaturas = random.randint(30, 84)
    elif tipo_instancia == 'Grandes':
        num_salas = random.randint(10, 25)
        num_asignaturas = random.randint(140, 300)
    else:
        raise ValueError("Tipo de instancia no válido. Debe ser 'Medianas' o 'Grandes'.")
    
    return num_asignaturas, num_salas

# Función para generar listas de asignaturas y salas
def generar_instancia(num_asignaturas, num_salas):
    asignaturas = []
    salas = []

    # Generación de salas con capacidades aleatorias entre 20 y 45 estudiantes
    for i in range(num_salas):
        capacidad = random.randint(20, 45)
        salas.append({'id': i + 1, 'capacidad': capacidad})

    # Generación de asignaturas con atributos aleatorios
    for i in range(num_asignaturas):
        prioridad = random.randint(1, 10)
        tipo = 'Teórica' if random.random() < 0.5 else 'Práctica'
        num_alumnos = random.randint(10, 40)
        bloques = 2 if random.random() < 0.65 else 1
        interes = random.randint(10, 40)
        asignaturas.append({
            'id': i + 1,
            'prioridad': prioridad,
            'tipo': tipo,
            'num_alumnos': num_alumnos,
            'bloques': bloques,
            'interes': interes
        })
    
    return asignaturas, salas

# Función para exportar a formato .mzn
def exportar_a_mzn(asignaturas, salas, filename_mzn):
    # Generación del archivo de texto
    with open(filename_mzn, 'w') as f:
        f.write("% Conjuntos\n")
        f.write("set of int: C = 1..{};\n".format(len(asignaturas)))  # Cursos
        f.write("set of int: S = 1..{};\n".format(len(salas)))  # Salas
        f.write("set of int: T = 1..35;  % Bloques de tiempo (1 a 35, 7 por día, 5 días)\n\n")

        f.write("% Parámetros\n")
        f.write("array[C] of int: pc = [\n")
        f.write(",\n".join(str(asignatura['prioridad']) for asignatura in asignaturas))
        f.write("];\n\n")

        f.write("array[S] of int: rs = [\n")
        f.write(",\n".join(str(sala['capacidad']) for sala in salas))
        f.write("];\n\n")

        f.write("array[C] of int: ic = [\n")
        f.write(",\n".join(str(asignatura['interes']) for asignatura in asignaturas))
        f.write("];\n\n")

        f.write("array[C] of int: b = [\n")
        f.write(",\n".join(str(asignatura['bloques']) for asignatura in asignaturas))
        f.write("];\n\n")

        f.write("% Variables de decisión\n")
        f.write("array[C, S, T] of var 0..1: xcst;  % 1 si el curso c está asignado a la sala s en el bloque t\n\n")

        f.write("% Función objetivo: maximizar la suma de prioridades de los cursos asignados\n")
        f.write("var int: objective = sum(c in C, s in S, t in T)(pc[c] * xcst[c, s, t]);\n\n")

        f.write("% Restricciones\n")
        f.write("constraint\n")
        f.write("    % Restricción de Bloques Consecutivos\n")
        f.write("    forall(c in C, s in S, t in T where t < max(T)) (\n")
        f.write("        (b[c] = 2) -> (xcst[c, s, t] + xcst[c, s, t + 1] + xcst[c, s, t - 1] <= b[c])\n")
        f.write("    );\n\n")

        f.write("constraint\n")
        f.write("    % Restricción de Capacidad de Sala\n")
        f.write("    forall(c in C, s in S, t in T) (\n")
        f.write("        xcst[c, s, t] * ic[c] <= rs[s]\n")
        f.write("    );\n\n")

        f.write("constraint\n")
        f.write("    % Restricción de No Solapamiento\n")
        f.write("    forall(s in S, t in T) (\n")
        f.write("        sum(c in C)(xcst[c, s, t]) <= 1\n")
        f.write("    );\n\n")

        f.write("constraint\n")
        f.write("    % Restricción de Distribución de Bloques\n")
        f.write("    sum(c in C)(if b[c] = 2 then 1 else 0 endif) >= 0.65 * card(C);\n\n")

        f.write("constraint\n")
        f.write("    % Asegurar que los cursos indispensables tengan sala asignada\n")
        f.write("    forall(c in C where pc[c] >= 6) (\n")
        f.write("        sum(s in S, t in T)(xcst[c, s, t]) = b[c]\n")
        f.write("    );\n\n")

        f.write("constraint\n")
        f.write("    % Asegurar que haya un mínimo de 7 bloques y máximo de 21 bloques en la semana\n")
        f.write("    let {\n")
        f.write("        var int: total_blocks = sum(c in C, s in S, t in T)(xcst[c, s, t])\n")
        f.write("    } in\n")
        f.write("    (7 <= total_blocks /\ total_blocks <= 21);\n\n")

        f.write("% Resolver el modelo\n")
        f.write("solve maximize objective;\n\n")

        f.write("% Mostrar resultados\n")
        f.write('output ["Asignación de cursos a salas y bloques de tiempo:\\n", show(xcst)];\n')

# Generador de instancias y análisis
def generar_y_exportar_instancias(tipo_instancia, num_instancias):
    for i in range(num_instancias):
        num_asignaturas, num_salas = num_salas_asig(tipo_instancia)
        asignaturas, salas = generar_instancia(num_asignaturas, num_salas)
        exportar_a_mzn(asignaturas, salas, f'instancia_{tipo_instancia}_{i+1}.mzn')

# Ejemplo de uso
generar_y_exportar_instancias('Medianas', 5)
generar_y_exportar_instancias('Grandes', 5)