require('dotenv').config();
const { ethers } = require("ethers");
const contractABI = require('../abi/contractABI.json');

// Proveedor local (nodo minero)
//const provider = new ethers.JsonRpcProvider("http://localhost:8545");

const contractAddress = process.env.CONTRACT_ADDRESS;
const provider = new ethers.JsonRpcProvider(process.env.NODE_URL);

module.exports = {
    contractAddress,
    contractABI,
    provider,
};
