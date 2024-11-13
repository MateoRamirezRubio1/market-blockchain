DO
$$
BEGIN
   IF NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'blockchainService') THEN
      CREATE DATABASE blockchainService;
   END IF;
EXCEPTION
   WHEN OTHERS THEN
      -- Si hay un error (por ejemplo, si la base de datos ya existe), lo ignoramos
      RAISE NOTICE 'Base de datos ya existe o no se pudo crear';
END
$$;


CREATE DATABASE blockchainService;

\c blockchainService;

CREATE TABLE IF NOT EXISTS blockchain_users (
    id VARCHAR(255) PRIMARY KEY, -- ID del usuario proporcionado por el microservicio de usuarios
    public_key VARCHAR(255) NOT NULL UNIQUE, -- La clave pública del usuario, debe ser única e inmutable
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Marca de tiempo de creación
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Marca de tiempo de actualización
);