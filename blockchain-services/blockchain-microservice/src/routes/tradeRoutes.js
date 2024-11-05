const express = require('express');
const tradeController = require('../controllers/tradeController');
const router = express.Router();

router.post('/', tradeController.createTrade);

// Ruta para obtener un trade por ID
router.get('/:id', tradeController.getTradeById);

module.exports = router;
