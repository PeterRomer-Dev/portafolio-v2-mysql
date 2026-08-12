# 1. Imagen base oficial de Python (ligera y optimizada para producción)
FROM python:3.10-slim

# 2. Variables de entorno de Python
# Evita que Python genere archivos .pyc en el contenedor y asegura logs en tiempo real
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Crear y definir el directorio de trabajo dentro del contenedor
WORKDIR /app

# 4. Instalar librerías del sistema necesarias para compilar paquetes de Python y SSL
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libssl-dev \
    && rm -rf /var/lib/apt-get/lists/*

# 5. Copiar e instalar las dependencias de Python (aprovecha la caché de Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copiar todo el código fuente del proyecto al contenedor
COPY . .

# 7. Exponer el puerto 5000 (puerto interno estándar para la app)
EXPOSE 5000

# 8. Comando para iniciar la aplicación Flask en producción usando Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]