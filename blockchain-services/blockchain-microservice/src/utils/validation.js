const Joi = require('joi');

const validateCreateTrade = (data) => {
    const schema = Joi.object({
        userId: Joi.string().required(),
        buyer: Joi.string().required(),   // Dirección del comprador (address)
        energyAmount: Joi.number().required(),  // Cantidad de energía negociada (kWh)
        pricePerEnergyUnit: Joi.number().required(),  // Precio por unidad de energía
        contractTermsHash: Joi.string().required()  // Hash de los términos del contrato
    });
    return schema.validate(data);
};

const validateGetTradeById = (data) => {
    const schema = Joi.object({
        tradeId: Joi.string().required()
    });
    return schema.validate(data);
};

module.exports = {
    validateCreateTrade,
    validateGetTradeById
};
