FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y ffmpeg

# Set working directory
WORKDIR /app

# Copy code
COPY . /app

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose Streamlit default port
EXPOSE 7860

# Run the Streamlit app
CMD ["streamlit", "run", "app_spam.py", "--server.port=7860", "--server.address=0.0.0.0"]
