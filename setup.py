from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="autopm",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Autonomous Project Management Assistant for Technical Program Managers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/autopm",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Office/Business :: Project Management",
    ],
    python_requires='>=3.8',
    install_requires=[
        'python-dotenv>=1.0.0',
        'slack-sdk>=3.21.3',
        'jira>=3.4.0',
        'notion-client>=2.0.0',
        'openai>=1.0.0',
        'python-crontab>=3.0.0',
        'pydantic>=2.0.0',
        'python-dateutil>=2.8.2',
        'requests>=2.31.0',
        'langchain>=0.0.300',
        'tqdm>=4.65.0',
        'pytz>=2023.3',
        'apscheduler>=3.10.1',
    ],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'black>=23.0.0',
            'isort>=5.12.0',
            'mypy>=1.0.0',
            'pylint>=2.17.0',
            'pytest-cov>=4.0.0',
            'pre-commit>=3.0.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'autopm=main:main',
        ],
    },
)
