import hashlib
import random


def generate_unique_name(sale_id: int, buyer_id: int, seller_id: int):
    # Concatenar los valores de los identificadores para que sean únicos
    unique_string = f"{sale_id}-{buyer_id}-{seller_id}"

    # Crear un hash SHA-256 de la cadena única
    sha256_hash = hashlib.sha256(unique_string.encode()).hexdigest()
    restante = 1 if (64 - len(sha256_hash)) == 0 else (64 - len(sha256_hash))

    # Tomar los primeros 32 caracteres del hash y agregar ceros al final para ajustarlo a 64 caracteres
    unique_id = "0x" + sha256_hash[:32] + "0" * 32

    return f"{unique_id}"


# Ejemplo de uso
id_venta = 266
id_usuario = "20815639-1010-4ec8-bd2f-6b33aa3cd1ea"
id_vendedor = "dasdsadasdsadadasdasdd32423423--0"

nombre_unico = generate_unique_name(id_venta, id_usuario, id_vendedor)
random_bool = random.choice([True, False])
print(nombre_unico, random_bool, type(random_bool))

"""
0xDDB32C16298B63087668F570817A297A00000000000000000000000000000000
0xA125C49E261C65F057EA5C7262C2DC7900000000000000000000000000000000

{
    "seller_id": "20815639-1010-4ec8-bd2f-6b33aa3cd1ea",
    "energy_amount": 3423,
    "price_per_unit": 3,
    "offer_type": "buy",
    "expiration_time": "2024-11-10T08:49:40.353000",
    "transfer_datetime": "2024-11-10T08:49:40.353000",
    "terms_conditions": "The seller agrees to deliver the specified amount of energy within the agreed time frame. The buyer is responsible for making the payment within 24 hours of receiving the energy. In case of any delay in payment or failure to deliver the energy, a penalty of 5% of the total transaction value will be applied for each day of delay.",
    "id": 1,
    "status": "accepted",
    "created_at": "2024-11-13T05:07:10.037558",
    "last_updated": "2024-11-13T05:38:52.965677",
    "buyer_id": "c9d8ab37-63a3-4710-b065-b5bb1e883b37"
}


{
  "offer_id": 1,
  "status": "pending",
  "penalty_reason": "The buyer failed to make the payment within the agreed 24-hour period, causing a delay in the transaction.",
  "id": 6,
  "confirmation_date": "2024-11-13T05:38:52.940998",
  "last_updated": "2024-11-13T05:38:52.953165",
  "offer": {
    "seller_id": "20815639-1010-4ec8-bd2f-6b33aa3cd1ea",
    "energy_amount": 3423,
    "price_per_unit": 3,
    "offer_type": "buy",
    "expiration_time": "2024-11-10T08:49:40.353000",
    "transfer_datetime": "2024-11-10T08:49:40.353000",
    "terms_conditions": "The seller agrees to deliver the specified amount of energy within the agreed time frame. The buyer is responsible for making the payment within 24 hours of receiving the energy. In case of any delay in payment or failure to deliver the energy, a penalty of 5% of the total transaction value will be applied for each day of delay.",
    "id": 1,
    "status": "accepted",
    "created_at": "2024-11-13T05:07:10.037558",
    "last_updated": "2024-11-13T05:38:52.965677",
    "buyer_id": "c9d8ab37-63a3-4710-b065-b5bb1e883b37"
  },
  "pdf_document_path": "0xc0820c0b57c111f16c817f90fd9373ea00000000000000000000000000000000"
}

"""
