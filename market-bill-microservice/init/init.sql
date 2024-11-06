CREATE DATABASE IF NOT EXISTS market_bill_microservice;

\c market_bill_microservice;

DROP TYPE IF EXISTS offertype;
DROP TYPE IF EXISTS offerstatus;

-- Crear el tipo enumerado OfferType
CREATE TYPE offertype AS ENUM ('buy', 'sell');

-- Crear el tipo enumerado OfferStatus
CREATE TYPE offerstatus AS ENUM ('draft', 'active', 'reserved', 'expired', 'cancelled', 'accepted', 'completed');

-- Crear la tabla offers
CREATE TABLE IF NOT EXISTS offers (
    id SERIAL PRIMARY KEY,
    seller_id INTEGER NOT NULL,  -- ID del vendedor
    buyer_id INTEGER,  -- ID del comprador, puede ser nulo
    energy_amount NUMERIC NOT NULL,  -- Cantidad de energía en kWh
    price_per_unit NUMERIC NOT NULL,  -- Precio por unidad de energía
    offer_type offertype NOT NULL,  -- Tipo de oferta (compra o venta)
    status offerstatus DEFAULT 'draft',  -- Estado de la oferta con valor predeterminado "draft"
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),  -- Fecha de creación
    expiration_time TIMESTAMP WITHOUT TIME ZONE NOT NULL,  -- Fecha de expiración de la oferta
    transfer_datetime TIMESTAMP WITHOUT TIME ZONE NOT NULL,  -- Fecha y hora del traspaso de energía
    terms_conditions VARCHAR NOT NULL,  -- Términos y condiciones
    last_updated TIMESTAMP WITHOUT TIME ZONE  -- Última actualización
);

-- Crear el tipo enumerado para el estado de la venta
CREATE TYPE sale_status AS ENUM ('pending', 'completed', 'penalized');

-- Crear la tabla sales
CREATE TABLE sales (
    id SERIAL PRIMARY KEY,
    offer_id INT NOT NULL UNIQUE REFERENCES offers(id),
    status sale_status DEFAULT 'pending',
    confirmation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    pdf_document_path VARCHAR NOT NULL,
    penalty_reason VARCHAR,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);