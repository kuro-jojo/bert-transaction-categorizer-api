# Use the official Python image
FROM python:3.11

# Set working directory
WORKDIR /app

# Copy app files
# COPY bert-transaction-model /app/bert-transaction-model
COPY requirements.txt /app/requirements.txt
COPY ./src /app/src

# Install dependencies
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
RUN pip install --no-cache-dir --upgrade torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Expose port
EXPOSE 8082

# Run the app
ENTRYPOINT ["fastapi", "run", "src/main.py"]
CMD ["--port", "8082"]
