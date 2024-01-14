import sys
import json

# Recupera los argumentos pasados al script
parametros_serializados = sys.argv[1]

# Deserializa los parámetros desde formato JSON
parametros = json.loads(parametros_serializados)

# Imprime los parámetros
print("Parámetros recibidos:", parametros)
