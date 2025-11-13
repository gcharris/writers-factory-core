"""Setup script for Writers Factory Core."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="writers-factory-core",
    version="0.1.0",
    author="Writers Factory Team",
    author_email="contact@writersfactory.io",
    description="A model-agnostic multi-agent novel writing system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gcharris/writers-factory-core",
    packages=find_packages(exclude=["tests", "docs", "examples"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Linguistic",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    extras_require={
        "dev": [
            "black>=23.12.1",
            "isort>=5.13.2",
            "flake8>=7.0.0",
            "mypy>=1.8.0",
        ],
        "test": [
            "pytest>=7.4.3",
            "pytest-asyncio>=0.21.1",
            "pytest-cov>=4.1.0",
            "pytest-mock>=3.12.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "factory=factory.ui.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
