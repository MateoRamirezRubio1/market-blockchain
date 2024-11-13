FROM nginx:latest

# Copia el archivo de configuración de Nginx al contenedor
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 8080

# Comando para ejecutar Nginx
CMD ["nginx", "-g", "daemon off;"]