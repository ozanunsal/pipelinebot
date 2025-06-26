import requests
import xml.etree.ElementTree as ET
import re
from .config import TESTING_FARM_API_TOKEN, TESTING_FARM_API_URL


def get_testing_farm_log(task_id):
    """
    Extract error information from Testing Farm XML results.
    task_id can be either a direct URL or a task ID that needs to be converted to URL.
    """
    try:

        # Append results.xml to get the XML results file
        xml_url = f"{task_id}/results.xml"

        # Fetch the XML results
        headers = (
            {"Authorization": f"Bearer {TESTING_FARM_API_TOKEN}"}
            if TESTING_FARM_API_TOKEN
            else {}
        )
        resp = requests.get(xml_url, headers=headers, timeout=30)
        resp.raise_for_status()

        # Parse XML content
        root = ET.fromstring(resp.content)
        # Extract error information from XML
        error_info = extract_errors_from_xml(root)

        if error_info:
            return error_info
        else:
            return "No specific error information found in Testing Farm results."

    except requests.RequestException as e:
        return f"Error fetching Testing Farm results: {str(e)}"
    except ET.ParseError as e:
        return f"Error parsing Testing Farm XML: {str(e)}"
    except Exception as e:
        return f"Error processing Testing Farm results: {str(e)}"


def extract_errors_from_xml(root):
    """
    Extract error messages and test failures from Testing Farm XML results.
    """
    error_messages = []

    # Look for testcase elements
    for testcase in root.findall(".//testcase"):
        result = testcase.get("result")
        if result in ("failed", "error"):
            testcase_name = testcase.get("name", "Unknown Test")
            for log in testcase.findall(".//log"):
                if "failures" in log.get("name"):
                    failures_yaml = log.get("href")
                if "testout.log" in log.get("name"):
                    testout_log = log.get("href")
    if testout_log:
        try:
            # Fetch the testout.log content
            log_resp = requests.get(testout_log, timeout=30)
            log_resp.raise_for_status()
            return log_resp.text
        except requests.RequestException as e:
            error_messages.append(f"Error fetching testout.log: {str(e)}")
