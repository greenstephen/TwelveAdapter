from setuptools import setup, find_packages

setup(
    name="nautilus-twelvedata",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="High-performance TwelveData adapter for NautilusTrader",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/nautilus-twelvedata",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Rust",
        "Topic :: Office/Business :: Financial :: Investment",
    ],
    python_requires=">=3.10",
    install_requires=[
        "nautilus-trader>=1.230.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
            "black>=23.0",
            "flake8>=6.0",
        ],
        "analysis": [
            "pandas>=2.0",
            "matplotlib>=3.7",
        ],
    },
    keywords=[
        "trading",
        "finance",
        "nautilus-trader",
        "twelvedata",
        "market-data",
        "rust",
    ],
)
