# Basis-Image
FROM python:3.11-slim

# Setze das Arbeitsverzeichnis im Container
WORKDIR /app

# Kopiere die Abhängigkeitsdatei und installiere die Pakete
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Kopiere den restlichen Anwendungscode
COPY . .

# Exponiere den Port, auf dem FastAPI läuft
EXPOSE 8000

# Startkommando für die FastAPI-App
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
