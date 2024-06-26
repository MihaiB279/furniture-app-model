FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY model /app/model
COPY rest.py /app/
COPY classes_for_requests.py /app/
COPY resolv.py /app/
COPY requirements.txt /app/

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "rest:app", "--host", "0.0.0.0", "--port", "8000"]
