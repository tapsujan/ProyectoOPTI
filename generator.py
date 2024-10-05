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


# integrar el Solver
   # Función para exportar los datos generados a un archivo .dzn
def exportar_a_dzn(asignaturas, salas, num_bloques):
    with open("asignacion_salas.dzn", "w") as f:
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

    print(f"Instancia guardada en 'asignacion_salas.dzn'")
    return 

# Ejemplo de uso

num_asignaturas,num_salas=num_salas_asig()

num_dias = 5
num_bloques = 7 * num_dias

asignaturas, salas = generar_instancia(num_asignaturas, num_salas)

exportar_a_dzn(asignaturas, salas, num_bloques)
"""
print("Asignaturas:")
for a in asignaturas:
    print(a)

print("\nSalas:")
for s in salas:
    print(s)
"""
