from setuptools import setup, find_packages

setup(
    name="pipelinebot",
    version="0.1.0",
    description="A CLI bot to summarize GitLab pipeline failures using Gemini.",
    author="Ozan Unsal",
    packages=find_packages(),
    install_requires=[
        "requests",
        "colorama"
    ],
    entry_points={
        "console_scripts": [
            "pipelinebot=pipelinebot.cli:main"
        ]
    },
    python_requires=">=3.8",
) 