from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="ai-agentic-framework",
    version="0.1.0",
    author="Selva",
    author_email="",
    description="Production-ready AI Agentic Framework with composable components",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/selvamanigovindaraj/ai-agentic-framework",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.10",
    install_requires=requirements,
    extras_require={
        "dev": [
            "black>=23.12.0",
            "ruff>=0.1.9",
            "mypy>=1.7.1",
            "pre-commit>=3.6.0",
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
            "agentic=agentic_framework.cli:main",
        ],
    },
)
