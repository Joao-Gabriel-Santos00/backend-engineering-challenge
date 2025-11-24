from setuptools import setup, find_packages

setup(
    name="delivery-time-cli",
    version="1.0.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "delivery_time_cli=src.main:main",
        ],
    },
    python_requires=">=3.7",
)