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
    python_requires=">=3.10",
    
    # Core requirements based on actual imports
    install_requires=[
        "langchain-core>=0.0.1",
        "langchain-community>=0.0.1",
        "langchain-openai>=0.0.2",
        "langchain-text-splitters>=0.0.1",
        "langgraph>=0.0.1",
        "pydantic>=2.0.0",
        "pyyaml>=6.0.0",
    ],
    
    # Optional dependencies based on actual usage patterns
    extras_require={
        # Document processing and RAG
        "rag": [
            "pypdf>=3.0.0",
            "pdfplumber>=0.10.0",
            "sentence-transformers>=2.2.2",
            "faiss-cpu>=1.7.4",
        ],
        
        # LLM integration
        "llm": [
            "openai>=1.3.0",
            "lmstudio>=0.0.1",
            "python-dotenv>=1.0.0",
            "requests>=2.31.0",
            "langchain-huggingface>=0.0.1",
            "torch>=2.0.0",
            "transformers>=4.30.0",
        ],
        
        # Agent tools
        "agent": [
            "fastmcp>=0.0.1",
            "wikipedia-api>=0.5.0",
        ],
        
        # Development
        "dev": [
            "jupyter>=1.0.0",
            "pytest>=7.0.0",
            "black>=23.0.0",
        ],
    },
    
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)