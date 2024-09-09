# Use the official Ubuntu base image
FROM ubuntu:latest

# Set the working directory inside the container
WORKDIR /usr/app/src

# Set the locale environment variable
ARG LANG="en_US.UTF-8"

# Install necessary packages and clean up to reduce image size
RUN apt-get update && apt-get install -y --no-install-recommends \
    apt-utils \
    locales \
    python3-pip \
    python3-venv \
    python3-yaml \
    rsyslog \
    systemd \
    systemd-cron \
    sudo && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create a Python virtual environment
RUN python3 -m venv /usr/app/venv

# Activate the virtual environment and install dependencies
COPY requirements.txt ./
RUN /usr/app/venv/bin/pip install --upgrade pip && \
    /usr/app/venv/bin/pip install -r requirements.txt

# Copy the rest of the application files to the container
COPY ./ ./

# Activate the virtual environment and run the Streamlit app
CMD ["/usr/app/venv/bin/streamlit", "run", "App.py"]
