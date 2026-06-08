FROM python:3.11-slim

RUN apt-get update && apt-get install -y curl zstd && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://ollama.com/install.sh | sh

WORKDIR /app

COPY app.py .
COPY ollama_service.py .
COPY requirements.txt .

RUN pip install -r requirements.txt

COPY start.sh .
RUN chmod +x start.sh

CMD ["./start.sh"]