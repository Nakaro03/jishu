FROM python:3.9

WORKDIR /app

# 必要なパッケージのインストール
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install requests

COPY . .

CMD ["python", "crawle.py"]