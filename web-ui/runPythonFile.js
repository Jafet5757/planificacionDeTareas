const { exec } = require('child_process');

// Ruta del archivo Python que deseas ejecutar
const archivoPython = './../test.py';

// Parámetros de entrada
const parametros = [[[1, 3], [2, 3], [3]], [[3.5, 2, 0.5], [10, 1, 2], [0.2, 2, 4]]];

// Serializa los parámetros a formato JSON
const parametrosSerializados = JSON.stringify(parametros);

// Comando para ejecutar el script de Python
const comando = `python ${archivoPython} ${parametrosSerializados}`;

// Ejecuta el comando
exec(comando, (error, stdout, stderr) => {
    if (error) {
        console.error(`Error al ejecutar el comando: ${error}`);
        return;
    }
    console.log(`Salida del script de Python: ${stdout}`);
});
