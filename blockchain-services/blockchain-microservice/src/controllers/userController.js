const { createWallet } = require('../services/blockchainService');
const asyncHandler = require('express-async-handler');

// Crear un nuevo usuario con su clave pública/privada
const createUser = asyncHandler(async (req, res) => {
    const { id, ...userData } = req.body;

    if (!id) {
        return res.status(400).json({ message: 'User ID is required' });
    }

    try {
        const { user, secret } = await createWallet({ id, ...userData });

        res.status(201).json({
            message: 'User blockchain network credentials created successfully',
            userId: user.id,
            publicKey: user.publicKey,
            secret: secret,
        });
    } catch (error) {
        console.error('Error creating user:', error);
        res.status(500).json({ message: 'Error creating user', error: error.message });
    }
});

module.exports = { createUser };