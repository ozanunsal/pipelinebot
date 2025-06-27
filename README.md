# 🚀 PipelineBot

**Intelligent GitLab Pipeline Failure Analysis with AI-Powered Insights**

A smart CLI tool that automatically analyzes failed GitLab CI/CD pipeline jobs, extracts error logs from both regular jobs and Testing Farm integrations, and provides human-readable summaries with actionable fixes using Google's Gemini AI.

## ✨ Features

- 🔍 **Smart Job Analysis**: Automatically detects and analyzes failed pipeline jobs
- 🧪 **Testing Farm Integration**: Extracts error logs from Testing Farm XML reports
- 🤖 **AI-Powered Summaries**: Uses Gemini AI to generate concise, actionable failure summaries
- 🎨 **Beautiful CLI Output**: Colorized, human-friendly terminal output
- ⚡ **High Performance**: Caching, connection pooling, and optimized processing
- 🐳 **Container Ready**: Podman support for easy deployment
- 🔧 **Flexible Configuration**: Environment variables and config file support

## 🚀 Quick Start

```bash
# Install
pip install -e .

# Run
pipelinebot --project mygroup/myproject --pipeline 123456
```

## 📋 What You Get

Instead of digging through verbose logs, get instant insights like:

```
Job 1: build-and-test
Reason: Build failed due to missing dependency 'requests==2.28.0'
Possible Fixes: Update requirements.txt to include the missing dependency

Job 2: testing-farm-integration
Reason: Test suite failed with timeout after 30 minutes
Possible Fixes: Increase timeout threshold or optimize test performance
```

## 🛠️ Built With

- **Python 3.8+** - Core application
- **Google Gemini AI** - Intelligent log analysis
- **GitLab API** - Pipeline and job data
- **Testing Farm API** - Test result extraction
- **Podman** - Containerization support

## 📦 Installation

1. Clone the repo:
   ```bash
   git clone <repo-url>
   cd pipeline-bot
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Install as a package (editable mode recommended for development):
   ```bash
   pip install -e .
   ```

## 🔧 Configuration

Set your API tokens and endpoints in `pipelinebot/config.py` or via environment variables:
- `GITLAB_API_TOKEN`, `GITLAB_API_URL`
- `TESTING_FARM_API_TOKEN`, `TESTING_FARM_API_URL`

## 🐳 Containerization

Build the Container image:
```bash
podman build -t pipeline-bot .
```

Run the container:
```bash
podman run --rm pipeline-bot --project <project> --pipeline <pipeline_id>
```

**Note**: The container includes Gemini CLI for AI-powered analysis.

## 🏗️ Development

- All source code is in the `pipelinebot/` package directory
- CLI entry point is `pipelinebot/cli.py`
- Add tests in the `tests/` directory

## Setup

### Prerequisites

- Python 3.10+
- GitLab API token
- Testing Farm API token (optional)

### Environment Variables

Set the following environment variables:

- `GITLAB_API_TOKEN`: Your GitLab API token
- `GITLAB_API_URL`: GitLab API URL (default: https://gitlab.com/api/v4)
- `TESTING_FARM_API_TOKEN`: Testing Farm API token (optional)
- `TESTING_FARM_API_URL`: Testing Farm API URL (default: https://api.testing-farm.io/v0.1)

### Running with Docker

1. Build the container:
```bash
docker build -t pipelinebot .
```

2. Run the container with your API keys:
```bash
docker run -e GITLAB_API_TOKEN=your_gitlab_token \
           -e TESTING_FARM_API_TOKEN=your_testing_farm_token \
           pipelinebot --help
```

## Usage

```bash
pipelinebot <project_id> <pipeline_id>
```

Example:
```bash
pipelinebot 12345 67890
```

---

**Perfect for DevOps teams, CI/CD engineers, and anyone who wants to understand pipeline failures at a glance!** 🎯