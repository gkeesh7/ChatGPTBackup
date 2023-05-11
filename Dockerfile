# Use a base Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the script and requirements file
COPY main.py requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the backup script
CMD ["python", "main.py"]
