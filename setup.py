from setuptools import setup, find_packages
from pathlib import Path

this_dir = Path(__file__).parent
long_description = (this_dir / "README.md").read_text(encoding="utf-8")

setup(
    name="im2203",
    version="0.1.0",
    description="Teaching-focused examples and demos for software engineering with AI components",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="AD Ozbakir",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "fastmcp",
        "wikipedia-api",
        "lmstudio",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
