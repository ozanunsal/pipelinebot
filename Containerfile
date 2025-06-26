FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Install the package
RUN pip install .

# Create a non-root user with a proper home directory
RUN useradd --create-home --shell /bin/bash pipelinebot
# Install Gemini CLI
RUN npm install -g @google/gemini-cli

# Create Gemini settings file
RUN mkdir -p /home/pipelinebot/.gemini && \
    echo '{"theme": "GitHub Light", "selectedAuthType": "oauth-personal"}' > /home/pipelinebot/.gemini/settings.json && \
    chown -R pipelinebot:pipelinebot /home/pipelinebot/.gemini

# Set environment variables to control Gemini's cache location
ENV HOME=/home/pipelinebot
ENV GEMINI_CACHE_DIR=/home/pipelinebot/.gemini

USER pipelinebot

ENTRYPOINT ["pipelinebot"] 