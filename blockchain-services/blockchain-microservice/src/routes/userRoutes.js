const express = require('express');
const { createUser } = require('../controllers/userController');
const router = express.Router();

// Ruta para crear un nuevo usuario y generar sus claves
router.post('/', createUser);

module.exports = router;
