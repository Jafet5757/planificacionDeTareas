#Algoritmo genetico para asignacion de trabajos (cada uno con una cantidad de operaciones) a maquinas
# recibimos como paramtero: [operations, lateness_matrix, size_population, generations, machines, jobs]
import random
import matplotlib.pyplot as plt
import numpy as np
import sys
import json

def init_population(size_population, jobs, machines, operations):
    """
    Inicializa una poblacion de forma aleatoria
    :param size_population: tamaño de la poblacion
    :param jobs: cantidad de trabajos
    :param machines: cantidad de maquinas
    :param operations: arreglo con la cantidad de operaciones de cada trabajo
    :return: poblacion inicial (job, machine, operation)
    """
    population = []
    for i in range(size_population):
      #un job esta compuesta por la cadena 'j1o1' que representa la operacion 1 del trabajo 1
      #se genera una cadena por cada operacion de cada trabajo
      individual = []
      for j in range(jobs):
        for k in range(len(operations[j])):
          #asignamos una maquina aleatoria a la operacion
          individual.append(['j'+str(j+1)+'o'+str(operations[j][k]), random.randint(1, machines), operations[j][k]])
      population.append(individual)
    return population

def fitness(individual, lateness_matrix):
    """
    Calcula el fitness de un individuo
    :param individual: individuo a evaluar
    :param lateness_matrix: matriz de tardanza [machine][operation]
    :return: fitness del individuo
    """
    fitness = 0
    for i in range(len(individual)):
      #calculamos su matriz de tardanza real
      actual_lateness_matrix = actual_tardiness_matrix(individual, lateness_matrix)#[machine][row]
      #calculamos la mayor tardanza de la fila y esa es la que sumamos al fitness
      for row in range(len(actual_lateness_matrix[0])):
        max_lateness = 0
        for machine in range(len(actual_lateness_matrix)):
          if actual_lateness_matrix[machine][row] != 0:
            #Obtenemos su operacion y su maquina
            operation = actual_lateness_matrix[machine][row][2]
            machine = actual_lateness_matrix[machine][row][1]
            #obtenbemos su tardanza
            tardiness = lateness_matrix[machine-1][operation-1]
            if max_lateness < tardiness:
              max_lateness = tardiness
        fitness += max_lateness
    return fitness

#No se usa a menos que la tardanza real sea muy compleja
def fast_fitness(individual, lateness_matrix):
    """
    Calcula el fitness de un individuo de forma rapida ye heuristica
    :param individual: individuo a evaluar
    :param lateness_matrix: matriz de tardanza [machine][operation]
    :return: fitness del individuo
    """
    fitness = 0
    for i in range(len(individual)):
      #obtenemos la maquina y la operacion del individuo
      machine = individual[i][1]
      operation = individual[i][2]
      #sumamos la tardanza de la operacion
      fitness += lateness_matrix[machine-1][operation-1]
    return fitness

def actual_tardiness_matrix(individual, lateness_matrix, print_matrix=False):
    """
    Calcula la matriz de tardanza real de un individuo teniendo en cuenta las operaciones en paralelo
    :param individual: individuo a evaluar
    :param lateness_matrix: matriz de tardanza [machine][operation]
    :return: matriz de tardanza real del individuo
    """
    #inicializamos una matriz[machine][row] llena de ceros
    actual_lateness_matrix = [[0 for i in range(len(individual))] for j in range(len(lateness_matrix))]
    #recorremos el individuo
    for i in range(len(individual)):
      #obtenemos la maquina del individuo
      machine = individual[i][1]
      #obtenemos la tarea del individuo (compuesta por las primeras 2 letras del primer elemento de la lista)
      task = individual[i][0][:2]
      #guardamos al individuo en la matriz de tardanza real, en su respectiva maquina y en la ultima fila
      actual_lateness_matrix[machine-1][len(actual_lateness_matrix[machine-1])-1] = individual[i]
      #iteramos buscando si la fila anterior tiene algo y la movemos hacia atras
      for j in range(len(actual_lateness_matrix[machine-1])-1,0,-1):
        #comprobamos que j no sea la ultima fila
        if j > 0:
          #si la fila anterior no tiene algo lo movemos hacia atras
          if actual_lateness_matrix[machine-1][j-1] == 0:
            same_task = False
            #verificamos si en cualquier maquina de la fila anterior está la misma tarea
            for k in range(len(actual_lateness_matrix)):
              #si hay algo diferente de cero en la fila anterior
              if actual_lateness_matrix[k][j-1] != 0:
                #si la tarea es la misma
                if actual_lateness_matrix[k][j-1][0][:2] == task:
                  #si esta la misma tarea rompemos el for, no puede estar en la misma fila de la misma tarea
                  same_task = True
                  break
            #si la tarea es la misma no movemos nada y terminamos la busqueda hacia atras
            if same_task:
              break
            actual_lateness_matrix[machine-1][j-1] = actual_lateness_matrix[machine-1][j]
            actual_lateness_matrix[machine-1][j] = 0
          else:
            #tiene algo, entonces salimos del for, está lo más atrás posible
            break
    #si se quiere imprimir la matriz de tardanza real
    if print_matrix:
      print('\nMatriz real\n')
      for i in range(len(actual_lateness_matrix)):
        print(actual_lateness_matrix[i])
    return actual_lateness_matrix

def selection_by_tournament(population, rate=0.85):
    """
    Selecciona un individuo de la poblacion por torneo
    :param population: poblacion a seleccionar [individuo, fitness]
    :param rate: taza de seleccion
    :return: individuo seleccionado
    """
    # Creamos una nueva poblacion ordenada de forma aleatoria
    pair1 = random.sample(population, len(population))
    pair2 = random.sample(population, len(population))

    # Seleccionamos el individuo con mejor fitness
    parents = [
        max(pair1[i], pair2[i], key=lambda x: x[1]) if random.uniform(0, 1) <= rate
        else min(pair1[i], pair2[i], key=lambda x: x[1])
        for i in range(len(population))
    ]

    return parents

def order_crossover(parents):
    """
    Cruza dos individuos por orden
    :param parents: padres a cruzar
    :return: arreglo con los hijos
    """
    new_population = []
    # recorremos los padres avanzando de a dos
    for i in range(0, len(parents), 2):
      #verificamos que no se haya terminado la poblacion
      if i+1 >= len(parents):
        new_population.append(parents[i][0])
        break
      #obtenemos los padres
      p1 = parents[i][0]
      p2 = parents[i+1][0]
      #creamos los hijos
      child1 = create_child(p1,p2)
      child2 = create_child(p2,p1)
      #agregamos los hijos a la nueva poblacion
      new_population.append(child1)
      new_population.append(child2)
    return new_population
      
def create_child(p1,p2):
    """
    Crea un hijo a partir de dos padres
    :param p1: padre 1
    :param p2: padre 2
    :return: hijo
    """
    #extraemos una subcadena del padre 1
    start = random.randint(0, int(len(p1)/3))
    end = random.randint(start+1, len(p1)-1)
    sub_p1 = p1[start:end]
    #borramos del padre 2 las operaciones que estan en la subcadena del padre 1
    sub_p2 = list(p2)
    for j in range(len(sub_p2)):
      #si algun elemento de la subcadena del padre 1 esta en el padre 2 lo cambio por un -1
      #si el elemento en sub_p2[i][0] esta en sub_p1 lo cambio por un -1
      if sub_p2[j][0] in [x[0] for x in sub_p1]:
        sub_p2[j] = -1
    #creamos el hijo
    child = []
    for i in range(len(sub_p2)):
      if sub_p2[i] != -1:
        child.append(sub_p2[i])
      else:
        child.append(sub_p1.pop(0))
    return child

def mutation(population, machines, lateness_matrix, machineRate=0.1, orderRate=0.1):
    """
    Muta un individuo de la poblacion
    :param population: poblacion a mutar
    :param machines: cantidad de maquinas
    :param lateness_matrix: matriz de tardanza [machine][operation]
    :param machineRate: taza de mutacion de maquinas
    :param orderRate: taza de mutacion de orden
    :return: poblacion mutada
    """

    # Recorremos la poblacion para mutar las maquinas
    for i in range(len(population)):
      # Verificamos si el individuo muta
      if random.uniform(0, 1) <= machineRate:
        # Obtenemos la posicion a mutar
        pos = random.randint(0, len(population[i]) - 1)

        # Obtenemos la nueva maquina
        new_machine = random.randint(1, machines)

        # Vemos en que maquina tiene mejor fitness
        job = population[i][pos]

        # vemos que maquina tiene menor tardanza
        if lateness_matrix[job[1]-1][job[2]-1] > lateness_matrix[new_machine-1][job[2]-1]:
          population[i][pos][1] = new_machine

    # Recorremos la poblacion, esta vez para mutar el orden
    for i in range(len(population)):
      # Verificamos si el individuo muta
      if random.uniform(0, 1) <= orderRate:
        # Obtenemos las posiciones a mutar
        pos1 = random.randint(0, len(population[i]) - 1)
        pos2 = random.randint(0, len(population[i]) - 1)

        # Cambiamos el orden
        population[i][pos1], population[i][pos2] = population[i][pos2], population[i][pos1]

    return population


def main(size_population, jobs, machines, operations, lateness_matrix, generations):
    """
    Algoritmo genetico para asignacion de trabajos a maquinas
    :param size_population: tamaño de la poblacion
    :param jobs: cantidad de trabajos
    :param machines: cantidad de maquinas
    :param operations: arreglo con la cantidad de operaciones de cada trabajo
    :param lateness_matrix: matriz de tardanza [machine][operation]
    :param generations: cantidad de generaciones
    :return: mejor individuo
    """
    # Inicializamos las tazas
    machineRate = 0.2
    orderRate = 0.025
    selectionRate = 0.90

    # Inicializamos la poblacion
    population = init_population(size_population, jobs, machines, operations)

    # calculamos el fitness de cada individuo
    for i in range(len(population)):
      #agregamos el fitness a cada individuo
      population[i] = [population[i], fitness(population[i], lateness_matrix)]

    for g in range(generations):

      # seleccionamos los padres
      parents = selection_by_tournament(population, selectionRate)

      # cruzamos los padres
      new_population = order_crossover(parents)

      # mutamos la poblacion
      new_population = mutation(new_population, machines, lateness_matrix, machineRate, orderRate)

      # calculamos el fitness de cada individuo en la nueva poblacion
      for i in range(len(new_population)):
        #agregamos el fitness a cada individuo
        new_population[i] = [new_population[i], fitness(new_population[i], lateness_matrix)]
      
      # ocobinar la poblacion vieja con la nueva
      population.extend(new_population)

      # ordenamos la poblacion por fitness
      population.sort(key=lambda x: x[1])

      # seleccionamos los mejores individuos
      population = population[:size_population]

      # imprimimos el mejor individuo
      print(g, population[0])

    return population[0]


def grapher(individual, duration_matrix):
    """
    Grafica el individuo
    :param individual: individuo a graficar
    :param duration_matrix: matriz de duracion [machine][operation] es igual a la matriz de tardanza
    """
    # Crear un rango de posiciones para las barras
    posiciones = np.arange(len(individual[0]))

    # Crear el gráfico de barras
    fig, ax = plt.subplots()

    # Dibujar las barras
    for i in range(len(individual[0])):
      machine = individual[0][i][1]
      operation = individual[0][i][2]
      duration = duration_matrix[machine-1][operation-1]
      ax.bar([machine], [duration], 0.35, label=individual[0][i][0], color="#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), bottom=[i])

    # Añadir etiquetas, título y leyenda
    ax.set_xticks(posiciones + 0.35 / 2)
    ax.set_xticklabels(individual[0])
    ax.set_xlabel('Maquinas')
    ax.set_ylabel('Valores')
    ax.set_title('Gráfico de Barras Superpuestas con Inicio y Fin Diferentes')
    ax.legend()

    # Mostrar el gráfico
    plt.show()

# Recupera los argumentos pasados al script
parametros_serializados = sys.argv[1]

# Deserializa los parámetros desde formato JSON
parametros = json.loads(parametros_serializados)

operations = parametros[0]
lateness_matrix = parametros[1]
size_population = parametros[2]
generations = parametros[3]
machines = parametros[4]
jobs = parametros[5]

print("Parámetros recibidos:", parametros)
best_individual = main(size_population, jobs, machines, operations, lateness_matrix, generations)
actual_tardiness_matrix(best_individual[0], lateness_matrix, True)

# Ejecutamos el algoritmo
""" size_population = 100
jobs = 3
machines = 3
operations = [[1,3], [2,3], [3]]
lateness_matrix = [[3.5, 2, 0.5], [10, 1, 2], [0.2, 2, 4]]
generations = 300
best_individual = main(size_population, jobs, machines, operations, lateness_matrix, generations)
print('Mejor individuo: ', best_individual)
#grapher(best_individual, lateness_matrix)
actual_tardiness_matrix(best_individual[0], lateness_matrix, True) """