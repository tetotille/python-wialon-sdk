"""Setup script for the package."""

from setuptools import find_packages, setup

setup(
    name="wialon-sdk",
    version="0.4.5",
    packages=find_packages(),
    install_requires=[
        "requests>=2.32.3",
    ],
    entry_points={
        "console_scripts": [
            "wialon-sdk=wialon_sdk.__main__:main",
        ],
    },
    author="Jorge Tillería",
    author_email="jltilleriam@gmail.com",
    description="Python SDK for Wialon API",
    long_description=open("README.md").read(),  # noqa: PTH123, SIM115
    long_description_content_type="text/markdown",
    url="https://github.com/tetotille/wialon-sdk",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
