# 1. Use Python as the base image
FROM python:3.11-slim

# 2. Set the working directory
WORKDIR /app

# 3. Copy dependency list
COPY requirements.txt .

# 4. Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy application files
COPY . .

# 6. Default startup command
CMD ["python", "monitor.py"]
