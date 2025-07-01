from .gitlab_api import get_pipeline_jobs, get_job_log
from .testing_farm_api import get_testing_farm_log
from .lm_api import summarize_error
from colorama import Fore, Style, init
import re
import logging

# Configure logging
logger = logging.getLogger(__name__)

init(autoreset=True)

MAX_SUMMARY_LINES = 10
TESTING_FARM_KEYWORDS = ['testing-farm', 'testing_farm', 'testingfarm']


def is_testing_farm_job(job, log):
    """Optimized Testing Farm job detection."""
    # Check job name first (fastest)
    job_name = job.get('name', '').lower()
    if any(keyword in job_name for keyword in TESTING_FARM_KEYWORDS):
        return True
    
    # Check job tags
    tags = job.get('tags', [])
    if any(keyword in tag.lower() for keyword in TESTING_FARM_KEYWORDS for tag in tags):
        return True
    
    # Check log content for Testing Farm URL (most reliable)
    return bool(re.search(r'Testing Farm report: https://[^\s]+', log))


def highlight(text, color):
    """Apply color highlighting to text."""
    return f"{color}{text}{Style.RESET_ALL}"


def clean_summary(text):
    """Clean and truncate summary text."""
    if not text:
        return ""
    
    # Remove leading/trailing whitespace and collapse multiple blank lines
    lines = [line.strip() for line in text.strip().splitlines() if line.strip()]
    
    if len(lines) > MAX_SUMMARY_LINES:
        truncated_text = '\n'.join(lines[:MAX_SUMMARY_LINES])
        truncated_indicator = highlight('[Summary truncated]', Fore.RED)
        return truncated_text + "\n" + truncated_indicator
    
    return '\n'.join(lines)


def format_fixes(fixes_text):
    if not fixes_text:
        return ''
    # Split on newlines, semicolons, or numbered/bulleted lists
    lines = re.split(r'\n|;|\d+\.\s*|-\s+', fixes_text)
    # Remove empty lines and strip whitespace
    lines = [line.strip() for line in lines if line.strip()]
    # Add a number to each line
    return '\n'.join([f'  {i+1}. {line}' for i, line in enumerate(lines)])


def process_job(job, project):
    """Process a single job and return its summary."""
    name = job['name']
    job_id = job['id']
    
    try:
        # Get job log
        log = get_job_log(project, job_id)
        
        # Determine if it's a Testing Farm job and get appropriate error log
        if is_testing_farm_job(job, log):
            logger.info(f"Processing Testing Farm job: {name}")
            match = re.search(r'Testing Farm report: (https://[^\s]+)', log)
            if match:
                tf_report_url = match.group(1)
                error_log = get_testing_farm_log(tf_report_url)
            else:
                error_log = "Could not find Testing Farm report URL in job log."
        else:
            logger.info(f"Processing regular job: {name}")
            error_log = log
        
        # Get summary from Gemini
        summary = summarize_error(error_log)
        
        # Parse and clean the summary
        if 'Summary:' in summary and 'Possible Fixes:' in summary:
            parts = re.split(r'Summary:|Possible Fixes:', summary)
            summary_text = parts[1].strip() if len(parts) > 1 else summary
            fixes_text = parts[2].strip() if len(parts) > 2 else ''
        else:
            summary_text = summary
            fixes_text = ''
        
        # Clean and validate summaries
        summary_text = clean_summary(summary_text)
        fixes_text = clean_summary(fixes_text)
        
        # Fallback for verbose or log-like summaries
        if (len(summary_text.splitlines()) > MAX_SUMMARY_LINES or
            any(word in summary_text.lower() for word in ["traceback", "error:", "exception", "failed at"])):
            summary_text = highlight("[Summary not available or too verbose]", Fore.RED)
        
        return {
            'name': name,
            'summary': summary_text,
            'fixes': fixes_text
        }
        
    except Exception as e:
        logger.error(f"Error processing job {name}: {str(e)}")
        return {
            'name': name,
            'summary': f"Error processing job: {str(e)}",
            'fixes': ''
        }


def summarize_pipeline(project, pipeline_id):
    """Summarize failed jobs in a pipeline with optimized processing."""
    try:
        # Get pipeline jobs
        jobs = get_pipeline_jobs(project, pipeline_id)
        
        # Filter failed jobs early
        failed_jobs = [job for job in jobs if job['status'] == 'failed']
        
        if not failed_jobs:
            return highlight("All jobs passed! 🎉", Fore.GREEN)
        
        logger.info(f"Found {len(failed_jobs)} failed jobs to process")
        
        # Process jobs and build summary
        summary_lines = []
        for idx, job in enumerate(failed_jobs, 1):
            logger.info("Processing job {}/{}: {}".format(idx, len(failed_jobs), job['name']))
            
            result = process_job(job, project)
            
            summary_lines.append(
                "{}\n"
                "{} {}\n"
                "{}\n{}\n".format(
                    highlight('Job {}: {}'.format(idx, result['name']), Fore.CYAN),
                    highlight('Reason:', Fore.YELLOW), result['summary'],
                    highlight('Possible Fixes:', Fore.MAGENTA), format_fixes(result['fixes'])
                )
            )
        
        return "\n".join(summary_lines)
        
    except Exception as e:
        logger.error(f"Error summarizing pipeline: {str(e)}")
        return highlight(f"Error: Unable to summarize pipeline. {str(e)}", Fore.RED)
