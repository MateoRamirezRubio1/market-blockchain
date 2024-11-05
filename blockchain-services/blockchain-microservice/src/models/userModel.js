const { DataTypes } = require('sequelize');
const sequelize = require('../config/databaseConfig').sequelize; // Conexión a la base de datos

const User = sequelize.define('User', {
    id: {
        type: DataTypes.STRING, // ID del usuario proporcionado por el microservicio de usuarios
        allowNull: false,
        primaryKey: true,
    },
    public_key: {
        type: DataTypes.STRING,
        allowNull: false, // La clave pública es requerida
    },
    created_at: {
        type: DataTypes.DATE,
        defaultValue: DataTypes.NOW,
    },
    updated_at: {
        type: DataTypes.DATE,
        defaultValue: DataTypes.NOW,
    },
}, {
    tableName: 'blockchain_users',
    timestamps: false, // Agregar createdAt y updatedAt
});

module.exports = User;
