FROM python:3.8

# Sätt arbetskatalog
WORKDIR /app

# Kopiera filerna
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Kopiera applikationskod
COPY . .

# Exponera porten Flask kör på
EXPOSE 5000

# Kör Flask
CMD ["flask", "run", "--host=0.0.0.0"]