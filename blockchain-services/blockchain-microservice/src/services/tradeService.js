const { provider, contractABI, contractAddress } = require('../config/ethersConfig');
const { checkAndTransferEther } = require('../utils/etherUtils');
const ethers = require('ethers');
const getUserPrivateKey = require('../services/gcpSecretManagerService').accessSecret;
const getUserById = require('../services/blockchainService').getUserById;

const createTrade = async (userId, sellerId, tradeData) => {
    try {
        // Obtener la dirección del usuario a partir del ID
        const user = await getUserById(userId);
        const userAddress = user.public_key;

        // Crear instancia del contrato
        const wallet = new ethers.Wallet(await getUserPrivateKey(userId), provider);
        const contractABI = [
            {
                "inputs": [
                    {
                        "internalType": "address",
                        "name": "_buyer",
                        "type": "address"
                    },
                    {
                        "internalType": "uint32",
                        "name": "_energyAmount",
                        "type": "uint32"
                    },
                    {
                        "internalType": "uint32",
                        "name": "_pricePerEnergyUnit",
                        "type": "uint32"
                    },
                    {
                        "internalType": "uint32",
                        "name": "_tradeStart",
                        "type": "uint32"
                    },
                    {
                        "internalType": "bytes32",
                        "name": "_contractTermsHash",
                        "type": "bytes32"
                    }
                ],
                "name": "createTrade",
                "outputs": [
                    {
                        "internalType": "uint256",
                        "name": "",
                        "type": "uint256"
                    }
                ],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "anonymous": false,
                "inputs": [
                    { "indexed": true, "internalType": "uint256", "name": "tradeId", "type": "uint256" },
                    { "indexed": true, "internalType": "address", "name": "seller", "type": "address" },
                    { "indexed": true, "internalType": "address", "name": "buyer", "type": "address" },
                    { "internalType": "uint32", "name": "energyAmount", "type": "uint32" },
                    { "internalType": "uint32", "name": "pricePerEnergyUnit", "type": "uint32" },
                    { "internalType": "uint32", "name": "tradeStart", "type": "uint32" },
                    { "internalType": "bytes32", "name": "contractTermsHash", "type": "bytes32" }
                ],
                "name": "TradeCreated",
                "type": "event"
            }
        ];

        const contract = new ethers.Contract(contractAddress, contractABI, wallet);

        const currentTimestamp = Math.floor(Date.now() / 1000);

        // Obtener dirección publica del vendedor
        const seller = await getUserById(sellerId);
        const sellerPublicAddress = seller.public_key;

        console.log(sellerPublicAddress);

        tradeData.buyer = sellerPublicAddress;

        const gasEstimate = await contract.createTrade.estimateGas(
            sellerPublicAddress,
            tradeData.energyAmount,
            tradeData.pricePerEnergyUnit,
            currentTimestamp, // tradeStart como el tiempo actual
            tradeData.contractTermsHash
        );
        await checkAndTransferEther(userAddress, gasEstimate);

        // Crear la transacción firmada
        userBalance = await provider.getBalance(userAddress);
        console.log(`User balance in: ${userBalance}`);

        const tx = await contract.createTrade(
            sellerPublicAddress,
            tradeData.energyAmount,
            tradeData.pricePerEnergyUnit,
            currentTimestamp, // tradeStart como el tiempo actual
            tradeData.contractTermsHash
        );

        const receipt = await tx.wait();

        return receipt;
    } catch (error) {
        console.error('Error creating trade:', error);
        throw new Error(`Failed to create trade ${error}`);
    }
};

// Función para obtener un trade por ID
const getTradeById = async (tradeId) => {
    try {
        const contractABI = [
            {
                "inputs": [
                    {
                        "internalType": "uint256",
                        "name": "_tradeId",
                        "type": "uint256"
                    }
                ],
                "name": "getTradeById",
                "outputs": [
                    {
                        "internalType": "address",
                        "name": "buyer",
                        "type": "address"
                    },
                    {
                        "internalType": "address",
                        "name": "seller",
                        "type": "address"
                    },
                    {
                        "internalType": "uint32",
                        "name": "energyAmount",
                        "type": "uint32"
                    },
                    {
                        "internalType": "uint32",
                        "name": "tradeStart",
                        "type": "uint32"
                    },
                    {
                        "internalType": "uint8",
                        "name": "status",
                        "type": "uint8"
                    },
                    {
                        "internalType": "bytes32",
                        "name": "contractTermsHash",
                        "type": "bytes32"
                    },
                    {
                        "internalType": "uint32",
                        "name": "pricePerEnergyUnit",
                        "type": "uint32"
                    }
                ],
                "stateMutability": "view",
                "type": "function"
            },
        ];

        console.log(tradeId);
        // Crear instancia del contrato
        const contract = new ethers.Contract(contractAddress, contractABI, provider);

        // Llamar a la función getTradeById del contrato
        const trade = await contract.getTradeById(Number(tradeId));

        return {
            buyer: trade.buyer,
            seller: trade.seller,
            energyAmount: trade.energyAmount.toString(),
            tradeStart: trade.tradeStart.toString(),
            status: trade.status.toString(),
            contractTermsHash: trade.contractTermsHash,
            pricePerEnergyUnit: trade.pricePerEnergyUnit.toString(),
        };
    } catch (error) {
        console.error('Error fetching trade:', error);
        throw new Error(`Failed to fetch trade: ${error}`);
    }
};

module.exports = {
    createTrade,
    getTradeById,
};
