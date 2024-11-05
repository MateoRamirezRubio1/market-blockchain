const { SecretManagerServiceClient } = require('@google-cloud/secret-manager');
const client = new SecretManagerServiceClient();

const createSecret = async (userId, privateKey) => {
    const [secret] = await client.createSecret({
        parent: `projects/${process.env.GCP_PROJECT_ID}`,
        secretId: `user-${userId}-private-key`,
        secret: {
            replication: { automatic: {} },
        },
    });

    await client.addSecretVersion({
        parent: secret.name,
        payload: { data: Buffer.from(privateKey, 'utf-8') },
    });

    return secret;
};

const accessSecret = async (userId) => {
    const projectIdNumber = process.env.GCP_PROJECT_NUMBER;
    const secretId = `user-${userId}-private-key`

    const secretVersionName = `projects/${projectIdNumber}/secrets/${secretId}/versions/latest`;

    try {
        const [version] = await client.accessSecretVersion({ name: secretVersionName });
        const privateKey = version.payload.data.toString('utf-8');
        return privateKey;
    } catch (error) {
        console.error(`Error accessing secret: ${error.message}`);
        throw error;
    }
};

module.exports = { createSecret, accessSecret };
