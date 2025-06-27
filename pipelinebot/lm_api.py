import subprocess
import json
import logging
import os
from functools import lru_cache

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Optimized prompt template - created once
PROMPT_TEMPLATE = """You are an expert CI assistant analyzing job failure logs.

TASK: Analyze the provided error log and provide:
1. A concise summary of the main failure reason (1-2 sentences)
2. Up to 2 actionable suggestions or fixes

FOCUS: Extract only the most relevant error messages, ignore unrelated output.

OUTPUT FORMAT:
Summary: <brief failure summary>
Possible Fixes: <actionable suggestions>

Error log:
{log_text}

Summary and possible fixes:"""

@lru_cache(maxsize=100)
def summarize_error(log_text):
    """
    Summarize error logs using Gemini CLI with caching for efficiency.

    Args:
        log_text (str): The error log to analyze

    Returns:
        str: Summarized error information and suggested fixes
    """
    try:
        # Format the prompt with the log text
        prompt = PROMPT_TEMPLATE.format(log_text=log_text)  # Limit log size for efficiency

        # Optimized subprocess call
        result = subprocess.run(
            ["gemini", "-p", prompt],
            capture_output=True,
            text=True,
            timeout=30,
            check=False  # Don't raise exception on non-zero return code
        )

        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
        else:
            error_msg = result.stderr.strip() if result.stderr else "Unknown error"
            logger.warning(f"Gemini CLI failed: {error_msg}")
            return f"Error: Unable to analyze log. {error_msg}"

    except subprocess.TimeoutExpired:
        logger.error("Gemini request timed out")
        return "Error: Request timed out. Please try again."
    except FileNotFoundError:
        logger.error("Gemini CLI not found")
        return "Error: Gemini CLI not installed. Please install it first."
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return f"Error: {str(e)}"

def clear_cache():
    """Clear the summarization cache if needed."""
    summarize_error.cache_clear()
