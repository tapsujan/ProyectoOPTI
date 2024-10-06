% Conjuntos
set of int: C;  % Conjunto de cursos
set of int: S;  % Conjunto de salas
set of int: T;  % Conjunto de bloques de tiempo

% Parámetros
array[C] of int: D;  % Número de bloques requeridos por el curso c (1 o 2)
array[C] of int: pc;  % Prioridad del curso c
array[S] of int: rs;  % Capacidad de la sala s
array[C] of int: ic;  % Interés de estudiantes por el curso c

% Variables de decisión
array[C, S, T] of var 0..1: xcst;  % Variable binaria

% Función objetivo
var int: obj = sum(c in C)(sum(s in S)(sum(t in T)(pc[c] * xcst[c, s, t])));

% Restricciones
% Restricción de Bloques Consecutivos
constraint forall(c in C where D[c] = 2) (
    forall(t in T where t < max(T) - 1) (
        sum(s in S)(xcst[c, s, t]) + sum(s in S)(xcst[c, s, t + 1]) <= 2
    )
);

% Restricción de Capacidad de Sala
constraint forall(c in C, s in S, t in T) (
    xcst[c, s, t] = 1 -> rs[s] >= ic[c]
);

% Restricción de No Solapamiento
constraint forall(s in S, t in T) (
    sum(c in C)(xcst[c, s, t]) <= 1
);

% Restricción de Distribución de Bloques
constraint (sum(c in C where D[c] = 2)(1) >= 0.65 * card(C));
constraint (sum(c in C where D[c] = 1)(1) >= 0.35 * card(C));

% Asegurar que los cursos indispensables tengan sala asignada
constraint forall(c in C where pc[c] >= 6) (
    sum(s in S)(sum(t in T)(xcst[c, s, t])) = D[c]
);

% Solucion
solve maximize obj;

% Output
output [
    show(obj), "\n",
    "Asignaciones:\n",
    concat([show(c) ++ ": " ++ show([s | s in S, t in T where xcst[c, s, t] == 1]) ++ "\n" | c in C])
];