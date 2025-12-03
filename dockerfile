# Start from an official Python image based on Alpine
FROM python:3.11-alpine

# Define the working directory inside the container
WORKDIR /app

# IMPORTANT: Installation of FFmpeg (required by yt-dlp for audio extraction/conversion)
# apk is Alpine's package manager
RUN apk add --no-cache ffmpeg

# Copy files from the repository context (GitHub) to the container
COPY requirements.txt .
COPY main.py .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Default command to run when the container starts
# This executes the main script
CMD ["python", "main.py"]
