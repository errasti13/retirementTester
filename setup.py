from setuptools import setup, find_packages

setup(
    name="retirement_simulation",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "yfinance",
        "pandas",
        "numpy",
        "matplotlib"
    ],
    author="Jon Errasti",
    author_email="errasti13@gmail.com",
    description="A retirement portfolio simulation tool using historical market data.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/errasti13/retirement_simulation",  # Update with your actual repo
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "retirement-sim=retirement_simulation.scripts.run_simulation:main",
        ],
    },
)
