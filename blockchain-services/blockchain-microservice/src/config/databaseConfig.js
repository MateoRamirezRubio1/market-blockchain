const { Sequelize } = require('sequelize');
require('dotenv').config();

const sequelize = new Sequelize(
    process.env.DB_NAME,      // Nombre de la base de datos
    process.env.DB_USER,      // Usuario de la base de datos
    process.env.DB_PASSWORD,  // Contraseña del usuario
    {
        host: process.env.DB_HOST,         // Host de la base de datos (ej. localhost)
        dialect: 'postgres',                // Dialecto de la base de datos
        logging: false,                     // Configura a true para habilitar el logging de las consultas
    }
);

// Probar la conexión a la base de datos
const testConnection = async () => {
    try {
        await sequelize.authenticate();
        console.log('Connection to the database has been established successfully.');
    } catch (error) {
        console.error('Unable to connect to the database:', error);
    }
};

// Exportar el objeto sequelize para ser utilizado en otros módulos
module.exports = { sequelize, testConnection };
