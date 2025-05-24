FROM python:3.12-slim

# Instalar las dependencias necesarias del sistema
RUN apt-get update && \
    apt-get install -y libgl1 libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copia el código y los requisitos
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

# Puerto de exposición
EXPOSE 5000

# Comando de arranque
CMD ["python", "app.py"]


RUN apt-get update && apt-get install -y libgl1 libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
