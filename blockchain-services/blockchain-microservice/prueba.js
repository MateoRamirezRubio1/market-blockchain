const { ethers } = require("ethers");

async function createAccount() {
    // Crea una nueva cuenta
    const wallet = ethers.Wallet.createRandom();

    // Obtén la dirección y la clave pública
    const publicKey = wallet.publicKey; // Clave pública
    const address = wallet.address; // Dirección de la cuenta
    const mnemonic = wallet.privateKey; // Frase mnemotécnica

    // Muestra los resultados
    console.log("Public Key:", publicKey);
    console.log("Address:", address);
    console.log("Mnemonic:", mnemonic);
}

// Ejecuta la función
createAccount().catch((error) => {
    console.error("Error creating account:", error);
});
