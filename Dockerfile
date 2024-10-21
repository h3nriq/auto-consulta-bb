# Base image
FROM python:3.8-slim

# Set working directory
WORKDIR /app

# Copy the requirements.txt file and install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application's code
COPY . /app

# Command to run your application
CMD ["python", "bot.py"]