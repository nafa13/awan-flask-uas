# Gunakan image Python 3.9 yang slim
FROM python:3.9-slim

# Set working directory di dalam container
WORKDIR /app

# Install system dependencies yang dibutuhkan
RUN apt-get update && apt-get install -y \
    pkg-config \
    default-libmysqlclient-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy file requirements.txt
COPY requirements.txt .

# Install dependencies Python
RUN pip install --no-cache-dir -r requirements.txt

# Copy seluruh source code
COPY . .

# Buat folder uploads jika belum ada
RUN mkdir -p uploads

# Expose port Flask
EXPOSE 5000

# Perintah untuk menjalankan aplikasi
CMD ["python", "app.py"]
