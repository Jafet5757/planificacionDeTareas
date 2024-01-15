const generateDataButton = document.getElementById('generateData-btn');
const startButton = document.getElementById('start-btn');
const operations = [];
const lateness_matrix = [];

generateDataButton.addEventListener('click', () => { 
  const machines = document.getElementById('machines').value;
  const tasks = document.getElementById('tasks').value;
  // Generamos un numero de operaciones aleatorio entre 1 y 10
  const numberOfOperations = Math.floor(Math.random() * 10) + 1;

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