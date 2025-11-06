# MCP Chat Agent

A self-contained example of an LLM-powered chat agent using FastMCP and LM Studio.

## Prerequisites

- Python 3.8+  
- Install dependencies in your active environment:
  ```bash
  pip install fastmcp wikipedia-api lmstudio
  ```
- LM Studio 0.3.17 Build 11 (Windows app).

## 1. Start the MCP Tool Server

1. Open PowerShell or CMD and change into the monolithic folder:
   ```bash
   cd d:\Repos2\im2203\src\im2203\monolithic
   ```
2. Launch the MCP server:
   ```bash
   python server.py
   ```
3. You should see output like:
   ```
   INFO  FastMCP server listening on http://127.0.0.1:8000/mcp/
   ```

## 2. Launch the LLM Server in LM Studio

1. Open the **LM Studio** Windows application.
2. From the **Developer** menu select **Start server**.
3. In the dialog, choose your model and click **OK**. Do choose a model which enables tool use, such as qwen2.5-7b-instruct
4. Verify you get:
   ```
   [INFO] [LM STUDIO SERVER] Success! HTTP server listening on port 1234
   ```

## 3. Run the Chat Client

In a new terminal (still in the same folder):
```bash
python chat_agent.py
```
You will be prompted:
```
You (leave blank to exit):
```
Type your question (e.g., “Who is Spinoza?”) and press Enter.  
The bot will stream its response and log each turn to `chat_history.txt`.

## 4. Inspect the Conversation Log

Open `chat_history.txt` to see a timestamped transcript of the session:
```
[2025-08-06 15:03:12] user: Who is Spinoza?
[2025-08-06 15:03:13] assistant: Baruch Spinoza was a Dutch philosopher...
```

---

Feel free to:
- Tweak the system prompt in `prompts.py`  
- Add or modify tools in `tools.py`  
- Experiment with different LM Studio models
