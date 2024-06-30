# Usa un'immagine di base con Python
FROM python:3.9

# Installa tzdata per la configurazione del fuso orario
RUN apt-get update && apt-get install -y tzdata

# Imposta il fuso orario (sostituisci "Europe/Rome" con il fuso orario corretto se necessario)
RUN ln -snf /usr/share/zoneinfo/$TIMEZONE /etc/localtime && echo $TIMEZONE > /etc/timezone

# Imposta la directory di lavoro all'interno del container
WORKDIR /app

# Copia il file requirements.txt nella directory di lavoro
COPY requirements.txt .

# Installa i pacchetti elencati nel file requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Cancella il file requirements.txt
RUN rm requirements.txt

# Copia il codice dell'applicazione nella directory di lavoro
COPY ./app .

# Esponi la porta 5000 per l'applicazione Flask
EXPOSE 5000

# Avvia l'applicazione Flask
CMD ["python3", "-u", "./app.py"]
