import matplotlib.pyplot as plt
import numpy as np

# Datos de ejemplo
categorias = ['A', 'B', 'C', 'D']
inicio_valores1 = [1, 3, 2, 1]
fin_valores1 = [4, 7, 2, 5]
inicio_valores2 = [5, 5, 1, 4]
fin_valores2 = [6, 6, 3, 8]

# Definir el ancho de las barras
ancho_barra = 0.35

# Crear un rango de posiciones para las barras
posiciones = np.arange(len(categorias))

# Crear el gráfico de barras
fig, ax = plt.subplots()

# Dibujar las barras
barra1 = ax.bar(posiciones, fin_valores1, ancho_barra, label='Serie 1', color=(0.2, 0.4, 0.6, 0.7), bottom=inicio_valores1)
barra2 = ax.bar(posiciones, fin_valores2, ancho_barra, label='Serie 2', color=(0.8, 0.2, 0.2, 0.7), bottom=inicio_valores2)
barra3 = ax.bar([1], [2], ancho_barra, label='Serie 3', color='orange', bottom=[0])

# Añadir etiquetas, título y leyenda
ax.set_xticks(posiciones + ancho_barra / 2)
ax.set_xticklabels(categorias)
ax.set_xlabel('Categorías')
ax.set_ylabel('Valores')
ax.set_title('Gráfico de Barras Superpuestas con Inicio y Fin Diferentes')
ax.legend()

# Mostrar el gráfico
plt.show()
