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
      for i in range(len(actual_lateness_matrix)):
        print(actual_lateness_matrix[i])

#Pruebas
individual = [['j1o1', 2, 1], ['j1o3', 1, 3], ['j2o2', 3, 2], ['j2o3', 1, 3], ['j3o3', 1, 3]]
lateness_matrix = [[3.5, 2, 0.5], [0, 1, 2], [0, 2, 4]]

actual_tardiness_matrix(individual, lateness_matrix, True)