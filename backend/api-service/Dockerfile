# Usar una imagen base de Python
FROM python:3.9-slim

# Copiar los archivos de la app
COPY . /app
WORKDIR /app

# Instalar dependencias
RUN pip install -r requirements.txt

# Exponer el puerto
EXPOSE 5001

# Ejecutar el servicio Flask
CMD ["python", "app.py"]
