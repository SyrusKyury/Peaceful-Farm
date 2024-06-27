# Usa un'immagine di base con Python
FROM python:3.9

# Imposta la directory di lavoro all'interno del container
WORKDIR /app

# Copia il file requirements.txt nella directory di lavoro
COPY requirements.txt .

# Installa i pacchetti elencati nel file requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Cancello il file requirements.txt
RUN rm requirements.txt

# Copia il codice dell'applicazione nella directory di lavoro
COPY ./app .

# Esponi la porta 5000 per l'applicazione Flask
EXPOSE 5000

# Avvia l'applicazione Flask
CMD ["python3", "-u", "./app.py"]