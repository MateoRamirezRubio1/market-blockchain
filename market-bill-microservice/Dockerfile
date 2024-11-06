# Usamos la imagen oficial de Python 3.10 como base
FROM python:3.10-slim

# Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos el archivo de dependencias (requirements.txt) al contenedor
COPY requirements.txt .

# Instalamos las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos todo el contenido de la aplicación al contenedor
COPY . .

# Exponemos el puerto en el que FastAPI se ejecutará
EXPOSE 4000

# Comando para ejecutar FastAPI usando Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "4000"]
