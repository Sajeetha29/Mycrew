# 1. Use an official lightweight Python image
FROM python:3.11-slim

# 2. Set the working directory inside the container container
WORKDIR /app

# 3. Copy the requirements file from your deploy folder into the container
COPY requirements.txt .

# 4. Install dependencies directly into the container system
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy everything else from your deploy folder (code, configs, .env) into the container
COPY . .

# 6. Expose the port FastAPI runs on
EXPOSE 8000

# 7. Command to run your specific script when the container boots up
CMD ["uvicorn", "day4_crew_yaml:app", "--host", "0.0.0.0", "--port", "8000"]