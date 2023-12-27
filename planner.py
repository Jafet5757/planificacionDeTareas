#Algoritmo genetico para asignacion de trabajos (cada uno con una cantidad de operaciones) a maquinas

import random
import matplotlib.pyplot as plt
import numpy as np

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
      #obtenemos la maquina y la operacion del individuo
      machine = individual[i][1]
      operation = individual[i][2]
      #sumamos la tardanza de la operacion
      fitness += lateness_matrix[machine-1][operation-1]
    return fitness

import random

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

def mutation(population, machines, machineRate=0.1, orderRate=0.2):
    """
    Muta un individuo de la poblacion
    :param population: poblacion a mutar
    :return: poblacion mutada
    """

    # Recorremos la poblacion
    for i in range(len(population)):
        # Verificamos si el individuo muta
        if random.uniform(0, 1) <= machineRate:
            # Obtenemos la posicion a mutar
            pos = random.randint(0, len(population[i]) - 1)

            # Obtenemos la nueva maquina
            new_machine = random.randint(1, machines)

            # Cambiamos la maquina
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
    machineRate = 0.1
    orderRate = 0.2
    selectionRate = 0.85

    for g in range(generations):
      # Inicializamos la poblacion
      population = init_population(size_population, jobs, machines, operations)

      # calculamos el fitness de cada individuo
      for i in range(len(population)):
        #agregamos el fitness a cada individuo
        population[i] = [population[i], fitness(population[i], lateness_matrix)]

      # seleccionamos los padres
      parents = selection_by_tournament(population, selectionRate)

      # cruzamos los padres
      new_population = order_crossover(parents)

      # mutamos la poblacion
      new_population = mutation(new_population, machines, machineRate, orderRate)

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


# Ejecutamos el algoritmo
size_population = 100
jobs = 3
machines = 3
operations = [[1,3], [2,3], [3]]
lateness_matrix = [[3.5, 2, 0.5], [0, 1, 2], [0, 2, 4]]
generations = 100
best_individual = main(size_population, jobs, machines, operations, lateness_matrix, generations)
print('Mejor individuo: ', best_individual)