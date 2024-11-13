const ethers = require('ethers');
const { provider } = require('../config/ethersConfig');

// Dirección del administrador que puede transferir Ether a los usuarios
let privateKey = process.env.ADMIN_PRIVATE_KEY;

if (privateKey.startsWith('0')) {
    privateKey = '0x' + privateKey.substring(1); // Agregar 'x' si falta
}

const adminPrivateKey = privateKey

const adminWallet = new ethers.Wallet(adminPrivateKey, provider);

const checkAndTransferEther = async (userAddress, gasEstimate) => {
    console.log("In checkAndTransferEther");
    const gasPrice = (await provider.getFeeData()).gasPrice;
    const totalGasCostWithMargin = BigInt(Math.floor(Number(gasEstimate) * Number(gasPrice) * 1.000000007));
    // console.log(`Gas price: ${gasPrice.toString()}`);
    // console.log(`Total cost with margin: ${totalGasCostWithMargin.toString()}`);

    // Obtener saldo del usuario
    const userBalance = await provider.getBalance(userAddress);

    // Si el saldo es menor al costo del gas, transferir Ether desde la cuenta admin
    if (userBalance < totalGasCostWithMargin) {
        const tx = await adminWallet.sendTransaction({
            to: userAddress,
            value: totalGasCostWithMargin - userBalance
        });
        await tx.wait();
        console.log(`Transferred ${totalGasCostWithMargin.toString()} wei to ${userAddress}`);
    }
};

module.exports = {
    checkAndTransferEther
};
