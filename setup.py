from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="eventyay",
    version="0.1.0",
    author="Shivam Pawar",
    author_email="shivam.pawar.7217@example.com",
    description="A Python client library for the Eventyay API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shivam-pawar-7217/eventyay-python-sdk",
    project_urls={
        "Bug Tracker": "https://github.com/shivam-pawar-7217/eventyay-python-sdk/issues",
        "Documentation": "https://github.com/shivam-pawar-7217/eventyay-python-sdk/tree/master/docs",
        "Source Code": "https://github.com/shivam-pawar-7217/eventyay-python-sdk",
    },
    packages=find_packages(exclude=["tests", "tests.*", "examples", "examples.*"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.950",
        ],
    },
    keywords="eventyay api sdk client event management",
    include_package_data=True,
    zip_safe=False,
)
