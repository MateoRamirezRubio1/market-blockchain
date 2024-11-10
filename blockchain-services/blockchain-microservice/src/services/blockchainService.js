const ethers = require('ethers');
const { createSecret } = require('./gcpSecretManagerService');
const User = require('../models/userModel');

// Obtener un usuario por ID
const getUserById = async (userId) => {
    const user = await User.findOne({ where: { id: userId } });
    if (!user) {
        throw new Error('User not found');
    }
    return user;
};

const createWallet = async (userData) => {
    // Generar una clave pública y privada
    const wallet = ethers.Wallet.createRandom();

    try {
        console.log(wallet.address);
        // Crear el usuario en la base de datos con la clave pública
        const user = await User.create({
            id: userData.id,
            public_key: wallet.address,
        });

        console.log(user.public_key);

        // Solo si el usuario se crea con éxito, guardar la clave privada en GCP Secret Manager
        const secret = await createSecret(userData.id, wallet.privateKey);

        return { user, secret };
    } catch (error) {
        // Manejo de errores: si hay un error al crear el usuario, no crees el secreto
        console.error('Error creating user or secret:', error);
        throw new Error('Failed to create user and secret');
    }
};

module.exports = { getUserById, createWallet };