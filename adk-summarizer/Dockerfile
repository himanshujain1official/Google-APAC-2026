# 1. Use an official, lightweight Python image
FROM python:3.11-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy the dependencies file first (optimizes Docker caching)
COPY requirements.txt .

# 4. Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of your application code into the container
COPY . .

# 6. Expose the port Cloud Run expects
EXPOSE 5000

# 7. Command to run the application using Gunicorn (production server)
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app