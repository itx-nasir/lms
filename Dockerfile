FROM python:3.11-slim

# Install system dependencies required by WeasyPrint and common image libraries
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       libcairo2 \
       libpango-1.0-0 \
       libpangocairo-1.0-0 \
       libgdk-pixbuf2.0-0 \
       libffi-dev \
       shared-mime-info \
       fonts-liberation \
       libssl-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy only requirements first to leverage Docker cache
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . /app

# Copy and make entrypoint executable
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

ENV PYTHONUNBUFFERED=1
ENV PORT=8000

EXPOSE 8000

CMD ["/app/entrypoint.sh"]
