import matplotlib.pyplot as plt
import numpy as np

#input: [[['j1o1', 3, 1], ['j1o3', 1, 3], ['j2o2', 2, 2], ['j2o3', 1, 3], ['j3o3', 1, 3]], 2.5]
# [job, machine, operation] = [tag, posicion, duration]

# Datos de ejemplo
input = [[['j1o1', 3, 1], ['j1o3', 1, 3], ['j2o2', 2, 2], ['j2o3', 1, 3], ['j3o3', 1, 3]], 2.5]
duration_matrix = [[3.5, 2, 0.5], [0, 1, 2], [0, 2, 4]] # [machine][operation]

# Crear un rango de posiciones para las barras
posiciones = np.arange(len(input[0]))

# Crear el gráfico de barras
fig, ax = plt.subplots()

# Dibujar las barras
""" barra1 = ax.bar(posiciones, fin_valores1, ancho_barra, label='Serie 1', color=(0.2, 0.4, 0.6, 0.7), bottom=inicio_valores1)
barra2 = ax.bar(posiciones, fin_valores2, ancho_barra, label='Serie 2', color=(0.8, 0.2, 0.2, 0.7), bottom=inicio_valores2)
barra3 = ax.bar([1], [2], ancho_barra, label='Serie 3', color='orange', bottom=[0]) """

for i in range(len(input[0])):
  machine = input[0][i][1]
  operation = input[0][i][2]
  duration = duration_matrix[machine-1][operation-1]
  ax.bar([i], [duration], 0.35, label='Serie 1', color=(0.2, 0.4, 0.6, 0.7), bottom=[i])

# Añadir etiquetas, título y leyenda
ax.set_xticks(posiciones + 0.35 / 2)
ax.set_xticklabels(input[0])
ax.set_xlabel('Categorías')
ax.set_ylabel('Valores')
ax.set_title('Gráfico de Barras Superpuestas con Inicio y Fin Diferentes')
ax.legend()

# Mostrar el gráfico
plt.show()
