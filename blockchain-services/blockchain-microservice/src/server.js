const app = require('./app');
const { testConnection } = require('./config/databaseConfig');
const http = require('http');
require('dotenv').config();

const PORT = process.env.PORT || 3000;
const server = http.createServer(app);
// Probar conexión a la base de datos
testConnection();

server.timeout = 0;

// Levantar el servidor
server.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
