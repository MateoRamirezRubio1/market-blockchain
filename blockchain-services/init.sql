CREATE TABLE IF NOT EXISTS blockchain_users (
    id SERIAL PRIMARY KEY, -- ID del usuario proporcionado por el microservicio de usuarios
    public_key VARCHAR(255) NOT NULL UNIQUE, -- La clave pública del usuario, debe ser única e inmutable
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Marca de tiempo de creación
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Marca de tiempo de actualización
);