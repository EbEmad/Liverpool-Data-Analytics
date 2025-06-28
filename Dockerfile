FROM apache/airflow:2.9.1-python3.10

# Set environment variables
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMIUM_DRIVER=/usr/lib/chromium-browser/chromedriver



# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
USER root
RUN apt-get update && apt-get install -y wget unzip && \
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt install -y ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb && \
    apt-get clean
COPY run.sh /run.sh
RUN chmod +x /run.sh
USER airflow
# Upgrade webdriver-manager to latest version
RUN pip install --upgrade webdriver-manager selenium

CMD ["bash","run.sh"]