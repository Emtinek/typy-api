FROM python:3.10-slim

# Instalacja zależności systemowych
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    gnupg \
    curl \
    fonts-liberation \
    libnss3 \
    libxss1 \
    libappindicator1 \
    libasound2 \
    libgbm-dev \
    libgtk-3-0 \
    libxshmfence1 \
    libxi6 \
    xvfb \
    --no-install-recommends && rm -rf /var/lib/apt/lists/*


# Instalacja Google Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Zainstaluj ChromeDriver dopasowany do Chrome
RUN CHROME_VERSION=$(google-chrome-stable --version | awk '{print $3}' | cut -d'.' -f1) && \
    DRIVER_VERSION=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION") && \
    wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/${DRIVER_VERSION}/chromedriver_linux64.zip && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    rm /tmp/chromedriver.zip

# Ustaw PATH
ENV PATH="/usr/local/bin:$PATH"

# Ustaw katalog roboczy
WORKDIR /app
COPY . .

# Instalacja zależności Pythona
RUN pip install --no-cache-dir -r requirements.txt

# Uruchom aplikację przez gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:app"]
