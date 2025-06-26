import os

GITLAB_API_TOKEN = os.getenv("GITLAB_API_TOKEN")
GITLAB_API_URL = os.getenv("GITLAB_API_URL", "https://gitlab.com/api/v4")

TESTING_FARM_API_TOKEN = os.getenv("TESTING_FARM_API_TOKEN")
TESTING_FARM_API_URL = os.getenv("TESTING_FARM_API_URL", "https://api.testing-farm.io/v0.1")

