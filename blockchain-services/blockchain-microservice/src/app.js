const express = require('express');
const userRoutes = require('./routes/userRoutes');
const tradeRoutes = require('./routes/tradeRoutes')
const errorMiddleware = require('./middlewares/errorMiddleware');
require('dotenv').config();

const app = express();

app.use(express.json());

// Rutas de usuarios
app.use('/api/v1/users', userRoutes);

// Rutas de trades
app.use('/api/v1/trades', tradeRoutes);

// Middleware de manejo de errores
app.use(errorMiddleware);

app.get('/', (req, res) => {
    res.send('¡Api of the blockchain microservice working properly!');
});

module.exports = app;