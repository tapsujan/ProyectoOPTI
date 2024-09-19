# GRUPO 13 - Minizinc

# A=1, as salas de la universidad tienen una capacidad que oscila entre 20 y 45 
# estudiantes, además, cada curso tiene un interés que oscila entre 10 y 40 alumnos

# B=2, n 65 % de las asignaturas tendrá dos bloques de clases a la semana, el
# resto tendrá un bloque

import random

def generar_instancia(num_asignaturas, num_salas, num_dias, num_bloques):
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

# -                 -

# QUEDA PENDIENTE
# integrar el Solver
# testear resultados

# -                 -

# Ejemplo de uso
"""
num_asignaturas = 20
num_salas = 10
num_dias = 5
num_bloques = 7

asignaturas, salas = generar_instancia(num_asignaturas, num_salas, num_dias, num_bloques)

print("Asignaturas:")
for a in asignaturas:
    print(a)

print("\nSalas:")
for s in salas:
    print(s)
"""