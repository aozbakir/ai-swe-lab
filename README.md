# Companion code for OU/IM2203: Software Engineering with AI Components

This repository contains all the extended examples and demo code used in IM2203 — Software Engineering with AI Components

hese folders go beyond what’s in the lecture notes: they’re designed to help you understand, experiment with, and build your own AI-driven software systems.
You’ll see core architectural patterns, hands-on implementations, and step-by-step tools that you can adapt for your own projects and assignments.

📁 What's Inside?
Each folder is either:

- 🔧 A lecture-driven example — illustrating a core pattern or design principle
- 🚀 A task-focused demo — preparing you for coursework and real-world implementation

---

🗨️ agentic_chat/ — Agent-Based Chat with Tools + LLMs  
A minimal agentic chat system showing how to integrate FastMCP tool servers with LM Studio:
 - server.py – exposes Python functions (tools) like wiki_search via FastMCP
 - chat_agent.py – connects to LM Studio, streams tokens, invokes tools on-the-fly
 - prompts.py – stores reusable prompts to guide agent reasoning
 - tools.py – client-side code for calling external tools
 - ChatSession – manages the conversation, errors, and logs everything to chat_history.txt
 - 💡 Learn how to:
   - Chain LLM thinking with function calls
   - Maintain chat history and control tool use
   - Extend the system with new tools or prompts

---

🔎 rag/ — Retrieval-Augmented Generation Pipeline  
A modular RAG (Retrieval-Augmented Generation) system with CLI tools that:
- Ingests and preprocesses documents via configurable pipeline
- Chunks content using various strategies (character, recursive)
- Creates and manages FAISS vector store with embeddings
- Supports multiple search strategies (similarity, MMR)
- Provides interactive QA interface with timeout handling
- Configurable with LM Studio, OpenAI, or Hugging Face models
- 💡 Use this as a production-ready base for document QA systems

---

🧾 requirement_eng/ — LLM-Powered Requirements Engineering Assistant  
- An interactive assistant for managing software requirements:
- Elicits stakeholder needs through guided Q&A
- Converts informal input into structured templates
- Flags ambiguities, inconsistencies, and missing pieces
- Generates user stories, acceptance tests, and traceability matrices
- 💡 Use this to learn how LLMs can support early-stage software design

---

📊 auto_report/ — Automated Weekly Reporting System  
A data-processing and reporting pipeline that:
- Parses inconsistent Excel or CSV files
- Normalizes messy labels (e.g., fuzzy region names)Generates clean PDF summaries every week
- Handles scheduling, logging, and error management
- 💡 Adapt this pattern for any routine data-cleaning/reporting task

---

## Prerequisites

Make sure you have:
- Python 3.8 or later
- A virtual environment (recommended: venv or conda)

Install the core dependencies:
```bash
pip install fastmcp wikipedia-api lmstudio
```

For the RAG system, you'll also need:
```bash
pip install langchain langchain-openai faiss-cpu sentence-transformers pypdf pdfplumber
```

Some folders may have additional requirements; see their individual README files.

---

🧭 Why This Matters
You’ll be building your own AI-enhanced software in this course. These examples are more than code—they're:
- Templates to save you time
- Reference points to understand core ideas
- Launchpads for experimenting and extending
Start with the examples, run them, break them, fix them—then make them your own.