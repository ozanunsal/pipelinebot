import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import logging
from functools import lru_cache
from .config import GITLAB_API_TOKEN, GITLAB_API_URL

# Configure logging
logger = logging.getLogger(__name__)

# Configure session with retry strategy and connection pooling
session = requests.Session()

# Retry strategy
retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
)

# Configure adapter with retry strategy
adapter = HTTPAdapter(max_retries=retry_strategy, pool_connections=10, pool_maxsize=20)
session.mount("http://", adapter)
session.mount("https://", adapter)

# Set default headers
session.headers.update({
    "PRIVATE-TOKEN": GITLAB_API_TOKEN,
    "User-Agent": "PipelineBot/1.0"
})

@lru_cache(maxsize=50)
def get_pipeline_jobs(project, pipeline_id):
    """
    Get pipeline jobs with caching for efficiency.
    
    Args:
        project: GitLab project ID or path
        pipeline_id: Pipeline ID
        
    Returns:
        list: List of job dictionaries
    """
    try:
        url = f"{GITLAB_API_URL}/projects/{project}/pipelines/{pipeline_id}/jobs"
        
        logger.info(f"Fetching jobs for pipeline {pipeline_id}")
        resp = session.get(url, timeout=30)
        resp.raise_for_status()
        
        jobs = resp.json()
        logger.info(f"Retrieved {len(jobs)} jobs from pipeline {pipeline_id}")
        
        return jobs
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching pipeline jobs: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error fetching pipeline jobs: {str(e)}")
        raise

def get_job_log(project, job_id):
    """
    Get job log with optimized error handling.
    
    Args:
        project: GitLab project ID or path
        job_id: Job ID
        
    Returns:
        str: Job log content
    """
    try:
        url = f"{GITLAB_API_URL}/projects/{project}/jobs/{job_id}/trace"
        
        logger.info(f"Fetching log for job {job_id}")
        resp = session.get(url, timeout=60)  # Longer timeout for logs
        resp.raise_for_status()
        
        log_content = resp.text
        logger.info(f"Retrieved log for job {job_id} ({len(log_content)} characters)")
        
        return log_content
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching job log for job {job_id}: {str(e)}")
        return f"Error fetching job log: {str(e)}"
    except Exception as e:
        logger.error(f"Unexpected error fetching job log for job {job_id}: {str(e)}")
        return f"Error fetching job log: {str(e)}"

def clear_cache():
    """Clear the job cache if needed."""
    get_pipeline_jobs.cache_clear()
