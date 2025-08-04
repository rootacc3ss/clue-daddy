"""
Setup script for Clue Daddy application.
"""

from setuptools import setup, find_packages
import os

# Read requirements from requirements.txt
def read_requirements():
    requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    with open(requirements_path, 'r', encoding='utf-8') as f:
        requirements = []
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                requirements.append(line)
        return requirements

# Read README for long description
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "Clue Daddy - AI Assistant for Interviews, Sales, and More"

setup(
    name="clue-daddy",
    version="1.0.0",
    description="AI assistant for interviews, sales calls, meetings, and more",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    author="Clue Daddy Team",
    author_email="contact@cluedaddy.app",
    url="https://github.com/cluedaddy/clue-daddy",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'clue_daddy': [
            'prompts/*.md',
            'prompts/*.txt',
        ],
    },
    install_requires=read_requirements(),
    python_requires=">=3.8",
    entry_points={
        'console_scripts': [
            'clue-daddy=clue_daddy.app:main',
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Office/Business",
        "Topic :: Communications",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    keywords="ai assistant interview sales meeting presentation",
    project_urls={
        "Bug Reports": "https://github.com/cluedaddy/clue-daddy/issues",
        "Source": "https://github.com/cluedaddy/clue-daddy",
        "Documentation": "https://docs.cluedaddy.app",
    },
)