const tradeService = require('../services/tradeService');
const { validateCreateTrade, validateGetTradeById } = require('../utils/validation');

const createTrade = async (req, res) => {
    const userId = req.body.userId;
    const tradeData = req.body;

    const { error } = validateCreateTrade(tradeData);
    if (error) return res.status(400).json({ error: error.details[0].message });

    try {
        const receipt = await tradeService.createTrade(userId, tradeData);
        return res.status(201).json({ message: 'Trade created successfully', receipt });
    } catch (error) {
        return res.status(500).json({ error: `Failed to create trade ${error}` });
    }
};

const getTradeById = async (req, res) => {
    const tradeId = req.params.id; // Obtén el tradeId de los parámetros de la URL

    // Si tienes alguna validación para tradeId, puedes hacerla aquí
    const { error } = validateGetTradeById({ tradeId }); // (Opcional) Agrega validación aquí si tienes una

    if (error) return res.status(400).json({ error: error.details[0].message });

    try {
        const trade = await tradeService.getTradeById(tradeId);
        return res.status(200).json(trade);
    } catch (error) {
        return res.status(500).json({ error: `Failed to fetch trade: ${error.message}` });
    }
};

module.exports = {
    createTrade,
    getTradeById,
};
