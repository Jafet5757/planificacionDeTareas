const express = require('express');
const app = express();
const path = require('path');
const ejs = require('ejs');
const morgan = require('morgan');
const port = 3000;

// Configuracion de las vistas
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));
// Configuracion de los middlewares
app.use(morgan('dev'));
app.use(express.urlencoded({ extended: false }));
app.use(express.json());
// Configuracion de los archivos estaticos
app.use(express.static(path.join(__dirname, 'public')));


// Configuracion de las rutas
app.get('/', (req, res) => {
  res.render('index');
});

app.listen(port, () => {
  console.log(`Servidor Express escuchando en el puerto ${port}`);
});
