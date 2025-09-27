# 1. Usar una imagen base oficial de Python.
FROM python:3.9-slim

# 2. Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# 3. Copiar el archivo de requerimientos y luego instalar las dependencias
# (Hacemos esto en dos pasos para aprovechar el caché de Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copiar el resto del código de la aplicación
COPY . .

# 5. Exponer el puerto que usará Flask
EXPOSE 8080

# 6. El comando que se ejecutará cuando el contenedor inicie
CMD ["python", "app.py"]