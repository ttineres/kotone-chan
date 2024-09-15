# Use Python image
FROM python:3.11

# Set working directory in the container
WORKDIR /app

# Copy the requirments file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Run the script
CMD ["python", "kotone/bot.py"]
