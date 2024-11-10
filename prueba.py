import hashlib


def generate_unique_id(id_venta, id_usuario, id_vendedor):
    # Concatenar los valores de los identificadores para que sean únicos
    unique_string = f"{id_venta}-{id_usuario}-{id_vendedor}"

    # Crear un hash SHA-256 de la cadena única
    sha256_hash = hashlib.sha256(unique_string.encode()).hexdigest()

    # Tomar los primeros 32 caracteres del hash y agregar ceros al final para ajustarlo a 64 caracteres
    unique_id = "0x" + sha256_hash[:32] + "0" * 32

    return unique_id


# Ejemplo de uso
id_venta = 266
id_usuario = 11
id_vendedor = 333

nombre_unico = generate_unique_id(id_venta, id_usuario, id_vendedor)
print(nombre_unico)
