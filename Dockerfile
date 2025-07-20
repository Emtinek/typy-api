FROM python:3.10-slim

# Systemowe zależności
RUN apt-get update && apt-get install -y \
    wget unzip gnupg curl \
    fonts-liberation libnss3 libxss1 libappindicator1 libasound2 \
    libgbm-dev libgtk-3-0 libxshmfence1 libxi6 xvfb \
    --no-install-recommends && rm -rf /var/lib/apt/lists/*

# Chrome (z oficjalnego źródła Google)
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

# ChromeDriver (dokładnie ta sama wersja co Chrome: 138.0.7204.157)
RUN wget -O /tmp/chromedriver.zip https://storage.googleapis.com/chrome-for-testing-public/138.0.7204.157/linux64/chromedriver-linux64.zip && \
    unzip /tmp/chromedriver.zip -d /tmp/ && \
    mv /tmp/chromedriver-linux64/chromedriver /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver && \
    rm -rf /tmp/chromedriver.zip /tmp/chromedriver-linux64

# PATH
ENV PATH="/usr/local/bin:$PATH"

# Katalog roboczy
WORKDIR /app
COPY . .

# Instalacja zależności
RUN pip install --no-cache-dir -r requirements.txt

# Start aplikacji
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:app"]



