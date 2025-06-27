import argparse
import logging
from .summarizer import summarize_pipeline


def main():
    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    parser = argparse.ArgumentParser(
        description="Summarize failed GitLab pipeline jobs using TinyLlama."
    )
    parser.add_argument("--project", required=True, help="GitLab project ID or path")
    parser.add_argument("--pipeline", required=True, help="GitLab pipeline ID")
    args = parser.parse_args()

    summary = summarize_pipeline(args.project, args.pipeline)
    print("=" * 80)
    print("🚀 PIPELINE FAILURE ANALYSIS REPORT")
    print("=" * 80)
    print(summary)


if __name__ == "__main__":
    main()