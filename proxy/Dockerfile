FROM nginx:latest

# Copia el archivo de configuración de Nginx al contenedor
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Crea directorios para los certificados
RUN mkdir -p /etc/ssl/certs /etc/ssl/private

# Copia los certificados SSL al contenedor
COPY your-cert.pem /etc/ssl/certs/your-cert.pem
COPY your-key.pem /etc/ssl/private/your-key.pem
