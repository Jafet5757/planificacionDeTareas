const { exec } = require('child_process');
const actions = {}

// Ruta del archivo Python que deseas ejecutar
const archivoPython = './../plannerParameters.py';

actions.start = async(operations, lateness_matrix, machines, jobs) => { 
  // Parámetros de entrada
  const parametros = [
    operations,
    lateness_matrix,
    100,// size_population
    100,// generations
    machines,
    jobs
  ]

  // Serializa los parámetros a formato JSON
  const parametrosSerializados = JSON.stringify(parametros);

  // Comando para ejecutar el script de Python
  const comando = `python ${archivoPython} ${parametrosSerializados}`;

  // Ejecuta el comando de forma asíncrona y retorna el resultado
  return new Promise((resolve, reject) => {
    exec(comando, (error, stdout, stderr) => {
      if (error) {
        console.error(`Error al ejecutar el comando: ${error}`);
        reject(error);
      }
      resolve(stdout);
    });
  });
}

module.exports = actions;