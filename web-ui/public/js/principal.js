const generateDataButton = document.getElementById('generateData-btn');
const startButton = document.getElementById('start-btn');
const generateGraphButton = document.getElementById('generateGraph-btn');
const generateTimesButton = document.getElementById('generateTimes-btn');
const bootstrapColors = ['primary', 'secondary', 'success', 'danger', 'warning', 'info', 'light'];
const operations = [];
const lateness_matrix = [];
let real_matrix = [];

generateDataButton.addEventListener('click', () => { 
  const machines = document.getElementById('machines').value;
  const tasks = document.getElementById('tasks').value;
  // Generamos un numero de operaciones aleatorio entre 1 y 5
  const numberOfOperations = Math.floor(Math.random() * 5) + 1;

  //Generamos la matriz de tardanza y la matriz de operaciones con el siguiente formato y de forma aleatoria:
  /* operations = [[1,3], [2,3], [3]]
  lateness_matrix = [[3.5, 2, 0.5], [10, 1, 2], [0.2, 2, 4]] */

  //Generamos la matriz de operaciones
  for (let i = 0; i < tasks; i++) {
    operations.push([]);
    //Generamos un numero de operaciones aleatorio entre 1 y numberOfOperations
    const lim = Math.floor(Math.random() * numberOfOperations) + 1;
    //generamos un arreglo de 0 a lim con numeros aleatorios no repetidos
    const arr = _.sampleSize(_.range(1, numberOfOperations + 1), lim);
    operations[i] = arr;
  }

  //Generamos la matriz de tardanza
  for (let i = 0; i< machines; i++) {
    lateness_matrix.push([]);
    for (let j = 0; j < numberOfOperations; j++) {
      //Generamos un numero de tardanza aleatorio entre 0 y 10 redondeado a 2 decimales
      lateness_matrix[i].push((Math.random() * 10).toFixed(2));
    }
  }

  // Pintamos los datos en las tablas lateness_matrix-table y operations-table
  printData(operations, lateness_matrix);
})

const printData = (operations, lateness_matrix) => { 
  console.log('Operations:',operations);
  console.log('Lateness_matrix: ',lateness_matrix);
  // Pintamos los datos en las tablas lateness_matrix-table y operations-table
  const latenessTable = document.getElementById('lateness_matrix-table');
  const operationsTable = document.getElementById('operations-table');
  // Selecionamos el elemento tbody de cada tabla
  const latenessTableBody = latenessTable.querySelector('tbody');
  const operationsTableBody = operationsTable.querySelector('tbody');
  // Limpiamos las tablas
  latenessTableBody.innerHTML = '';
  operationsTableBody.innerHTML = '';
  // Pintamos los datos en las tablas
  operations.forEach((row, i) => {
    const tr = document.createElement('tr');
    row.forEach((col, j) => {
      const td = document.createElement('td');
      td.textContent = col;
      tr.appendChild(td);
    });
    // agregamos el html creado
    operationsTable.innerHTML += `<tr><td>J${i + 1}</td>${tr.innerHTML}</tr>`;
  });
  lateness_matrix.forEach((row, i) => {
    const tr = document.createElement('tr');
    row.forEach((col, j) => {
      const td = document.createElement('td');
      td.textContent = col;
      tr.appendChild(td);
    });
    // agregamos el html creado
    latenessTable.innerHTML += `<tr><td>M${i + 1}</td>${tr.innerHTML}</tr>`;
  });
}

startButton.addEventListener('click', () => { 
  // Hacemos una petición fetch a la ruta /start
  fetch('/start', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      operations,
      lateness_matrix,
      machines: lateness_matrix.length,
      jobs: operations.length
    })
  })
    .then(res => res.json())
    .then(res => {
      console.log(res);
      const result = document.getElementById('result');
      result.value = res.result;
    })
    .catch(err => console.log(err));
})

generateGraphButton.addEventListener('click', () => { 
  // Leemos la matriz de el textarea con id=actual_matrix
  const actual_matrix = document.getElementById('actual_matrix').value;
  // Convertimos la matriz de string a array, separando por saltos de linea
  const matrix = actual_matrix.split('\n');
  // Convertimos la matriz de string a array, con el formato [0, ['j3o3', 2, 3], 0, 0, 0, 0, 0, 0, 0, 0]
  const matrixArray = cadenaAMatriz(actual_matrix);
  real_matrix = matrixArray;
  console.log(matrixArray);
  const chart = document.getElementById('chart');
  // Recorremos la matriz y pintamos los datos en una tabla dentro de chart
  matrixArray.forEach((row, i) => {
    const tr = document.createElement('tr');
    row.forEach((col, j) => {
      const td = document.createElement('td');
      td.textContent = col;
      // agregamos el color de fondo aleatorio
      td.classList.add(`bg-${_.sample(bootstrapColors)}`);
      tr.appendChild(td);
    });
    // agregamos el html creado
    chart.innerHTML += `<tr><td>M${i + 1}</td>${tr.innerHTML}</tr>`;
  });
})

function cadenaAMatriz(cadena) {
  // Divide la cadena en líneas
  const lineas = cadena.trim().split('\n');

  // Convierte cada línea en un array
  const matriz = lineas.map((linea) => {
    // Si la línea contiene corchetes, la trata como una submatriz
    if (linea.includes('[') && linea.includes(']')) {
      // Transforma la submatriz en un array
      const submatriz = cadenaAArreglo(linea);
      // Devuelve la submatriz
      return submatriz;
    } else {
      // Si no hay corchetes, simplemente divide por comas
      return linea.split(',').map((elemento) => {
        // Si el elemento es una cadena, lo mantiene como está
        if (/\'|\"/.test(elemento)) {
          return elemento;
        }
        // Si es un número, lo convierte a número
        return Number(elemento);
      });
    }
  });

  return matriz;
}

function cadenaAArreglo(cadena) {
  // Eliminamos el primer y último elemento de la cadena
  cadena = cadena.slice(1, -1);
  // Separamos por corchetes usando expresiones regulares
  const subcadenas = cadena.split(/\[|\]/g);
  // Recorremos las subcadenas
  for (let i = 0; i < subcadenas.length; i++) {
    // Eliminamos los espacios en blanco
    subcadenas[i] = subcadenas[i].trim();
    // Si la subcadena está vacía, la eliminamos
    if (subcadenas[i] === '' || subcadenas[i] === ',') {
      subcadenas.splice(i, 1);
      i--;
    } else {
      // separamos por comas
      const subcadena = subcadenas[i].split(',');
      // Reemplazamos la subcadena por el arreglo
      subcadenas[i] = subcadena;
    }
  }
  return subcadenas;
}

generateTimesButton.addEventListener('click', () => { 
  // Usamos la real_matrix y la lateness_matrix para calcular los tiempos de inicio y fin de cada operación, los pintamos en una tabla
  const timesTable = document.getElementById('times-table');
  let accumulatedTime = 0;
  // Limpiamos la tabla
  timesTable.innerHTML = '';
  // recorremos la real_matrix
  for (let i = 0; i < real_matrix.length; i++) {
    // Recorremos la columna
    for (let j = 0; j < real_matrix[i].length; j++) {
      let operation = real_matrix[i][j];
      // si es una cadena
      if(typeof real_matrix[i][j] === 'string') {
        // Eliminamos los espacios en blanco y las comillas y las comas
        operation = real_matrix[i][j].replace(/\'|\"|\,/g, '').trim();
      }
      // si la operación diferente de 0 y no es vacía y no incluye ' 0'
      if (operation !== '0' && operation !== '' && !operation.includes(' 0')) {
        console.log('Operation: ', operation)
        // Entonces es un arreglo con el formato [id, maquina, numero de operacion]
        const maquina = Number(operation[1].replace(/\'|\"|\,/g, '').trim());
        const no = Number(operation[2].replace(/\'|\"|\,/g, '').trim());
        // Calculamos su tardanza en la matriz de tardanza
        const lateness = Number(lateness_matrix[maquina - 1][no - 1]);
        // Pintamos en la tabla
        timesTable.innerHTML += `
        <tr>
          <td>Maquina ${operation[1]}</td>
          <td>${operation[0]}</td>
          <td>${accumulatedTime}</td>
          <td>${lateness}</td>
        </tr>`;
        // Sumamos el tiempo total
        accumulatedTime += lateness;
      }
    }
  }
})