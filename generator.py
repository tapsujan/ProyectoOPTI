# GRUPO 13 - Minizinc

# A=1, as salas de la universidad tienen una capacidad que oscila entre 20 y 45 
# estudiantes, además, cada curso tiene un interés que oscila entre 10 y 40 alumnos

# B=2, n 65 % de las asignaturas tendrá dos bloques de clases a la semana, el
# resto tendrá un bloque

import random

def generar_instancia(num_asignaturas, num_salas):
    asignaturas = []
    for i in range(num_asignaturas):

        bloques = 0
        # 65% de las asignaturas serán de dos bloques
        if random.random() < 0.65:
            bloques = 2
        else:
            bloques = 1

        prioridad = 0
        tipo = ''
        # Cada 5 asignaturas, 1 es indispensable
        if i % 5 == 0:
            prioridad = random.randint(6, 10)
            tipo = 'indispensable'
        else:
            prioridad = random.randint(1, 5)
            tipo = 'opcional'
        
        num_alumnos = random.randint(10, 40)
        asignaturas.append({
            'id': i,
            'prioridad': prioridad,
            'tipo': tipo,
            'alumnos': num_alumnos,
            'bloques': bloques
        })

    salas = []
    for j in range(num_salas):
        capacidad = random.randint(20, 45)
        salas.append({
            'id': j,
            'capacidad': capacidad
        })

    return asignaturas, salas



def num_salas_asig():
    tipo_instancia = random.choice(['Mediana', 'Grande'])
    print(f"Tipo de instancia seleccionada: {tipo_instancia}")
    if tipo_instancia == 'Mediana':
        # Selección de cantidad de asignaturas y salas dentro de los rangos medianos
        num_salas = random.choice([3, 4, 5, 6, 7])
        if num_salas==3:
            num_asig=random.randint(30,35)
        elif num_salas==4:
            num_asig=random.randint(45,49)
        elif num_salas==5:
            num_asig = random.randint(60,64)
        elif num_salas==6:
            num_asig = random.randint(70,74)
        else:
            num_asig= random.randint(80,84)
        
    elif tipo_instancia == 'Grande':
        # Selección de cantidad de asignaturas y salas dentro de los rangos grandes
        num_asig = random.choice([random.randint(140, 160), random.randint(170, 190), random.randint(200, 220), random.randint(230, 250), random.randint(280, 300)])
        num_salas = random.choice([random.randint(10, 12), random.randint(13, 15), random.randint(16, 18), random.randint(19, 22), random.randint(23, 25)])
        if num_salas<=12 and num_salas>=10:
            num_asig=random.randint(140,160)
        elif num_salas<=15 and num_salas>=13:
            num_asig=random.randint(170,190)
        elif num_salas<=18 and num_salas>=16:
            num_asig = random.randint(200,220)
        elif num_salas<=22 and num_salas>=19:
            num_asig = random.randint(230,250)
        else:
            num_asig= random.randint(280,300)
            
    return num_asig, num_salas

            
# Función para exportar los datos generados a un archivo .dzn con el cual se trabajara en el Minizinc
def exportar_a_dzn(asignaturas, salas, num_bloques):
    with open("asignacion_salas2.dzn", "w") as f:
        # Escribir el número de cursos, salas y bloques
        f.write(f"num_cursos = {len(asignaturas)};\n")
        f.write(f"num_salas = {len(salas)};\n")
        f.write(f"num_bloques = {num_bloques};\n")
        
        # Escribir las prioridades de los cursos
        prioridades = [a['prioridad'] for a in asignaturas]
        f.write(f"prioridad = [{', '.join(map(str, prioridades))}];\n")
        
        # Escribir el interés (número de alumnos) de cada curso
        intereses = [a['alumnos'] for a in asignaturas]
        f.write(f"interes = [{', '.join(map(str, intereses))}];\n")
        
        # Escribir la capacidad de cada sala
        capacidades = [s['capacidad'] for s in salas]
        f.write(f"capacidad = [{', '.join(map(str, capacidades))}];\n")
        
        # Escribir los bloques necesarios para cada curso
        bloques_necesarios = [a['bloques'] for a in asignaturas]
        f.write(f"bloques_necesarios = [{', '.join(map(str, bloques_necesarios))}];\n")

    print(f"Instancia guardada en 'asignacion_salas2.dzn'")

#Creacion del modelo en miniZinc
# Guardar el archivo MiniZinc en 'asignacion_salas.mzn'
minizinc_code = """

 % Parámetros del problema
int: num_cursos;    % Número de cursos
int: num_salas;     % Número de salas
int: num_bloques;   % Número de bloques de tiempo disponibles

% Prioridad de cada curso
array[1..num_cursos] of int: prioridad;

% Interés de estudiantes en cada curso
array[1..num_cursos] of int: interes;

% Capacidad de cada sala
array[1..num_salas] of int: capacidad;

% Número de bloques requeridos por cada curso (1 o 2)
array[1..num_cursos] of int: bloques_necesarios;

% Variable de decisión: x[c, s, t] indica si el curso c está asignado a la sala s en el bloque t
array[1..num_cursos, 1..num_salas, 1..num_bloques] of var 0..1: x;

% Función objetivo: maximizar la prioridad de los cursos asignados a las salas
var int: total_prioridad = sum(c in 1..num_cursos, s in 1..num_salas, t in 1..num_bloques)
                           (prioridad[c] * x[c, s, t]);

solve maximize total_prioridad;

% Restricciones

% 1. Cada curso debe ser asignado a 1 o 2 bloques (según lo que necesite)
constraint
  forall(c in 1..num_cursos) (
    sum(s in 1..num_salas, t in 1..num_bloques) (x[c, s, t]) = bloques_necesarios[c]
  );

% 2. Una sala no puede ser asignada a más de un curso en el mismo bloque
constraint
  forall(s in 1..num_salas, t in 1..num_bloques) (
    sum(c in 1..num_cursos) (x[c, s, t]) <= 1
  );

% 3. La capacidad de la sala debe ser suficiente para el curso asignado
constraint
  forall(c in 1..num_cursos, s in 1..num_salas, t in 1..num_bloques) (
    x[c, s, t] = 1 -> capacidad[s] >= interes[c]
  );

% 4. Si un curso necesita dos bloques, deben ser consecutivos
constraint
  forall(c in 1..num_cursos, s in 1..num_salas, t in 1..num_bloques-1) (
    bloques_necesarios[c] = 2 -> (x[c, s, t] = 1 -> x[c, s, t + 1] <= 2)
  );
  
  
% 5. El 65% de los cursos debe tener dos bloques
constraint
  sum(c in 1..num_cursos) (bloques_necesarios[c] = 2) >= 0.65 * num_cursos;


% 6. Asegurar que los cursos indispensables tengan una sala asignada
constraint
  forall(c in 1..num_cursos where prioridad[c] >= 6) (
    sum(s in 1..num_salas, t in 1..num_bloques) (x[c, s, t]) = bloques_necesarios[c]
  );


"""

with open('asignacion_salas.mzn', 'w') as f:
    f.write(minizinc_code)



#Ejemplo de uso
num_asignaturas,num_salas=num_salas_asig()

num_dias = 5
num_bloques = 7 * num_dias

asignaturas, salas = generar_instancia(num_asignaturas, num_salas)

exportar_a_dzn(asignaturas, salas, num_bloques)
           

# Utilizar Minizinc para probar                 -

# Ejemplo de uso
"""
print("Asignaturas:")
for a in asignaturas:
    print(a)

print("\nSalas:")
for s in salas:
    print(s)
"""
