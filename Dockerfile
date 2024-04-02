# Base image
FROM python:3.8-slim

# Install utilities
RUN apt-get update && apt-get install -y wget gnupg2 unzip \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Add Google Chrome repository
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list

# Install Google Chrome
RUN apt-get update && apt-get install -y google-chrome-stable

# Set working directory
WORKDIR /app

# Copy the requirements.txt file and install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application's code
COPY . /app

# Command to run your application
CMD ["python", "bot.py"]
