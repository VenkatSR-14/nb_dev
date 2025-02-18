# Use official Python image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy only requirements first for better caching
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend source code
COPY . . 

# Expose FastAPI port
EXPOSE 8000

# Run FastAPI application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
