# Python MCP Server – Hello MCP

A beginner-friendly Model Context Protocol (MCP) server built using Python 3.12, the MCP Python SDK, and Visual Studio Code.

## 1. Project Overview

This project demonstrates how to build a local Python MCP server that exposes Python functions as tools for AI applications.

The server uses **stdio (Standard Input/Output)** transport and is designed to integrate with Visual Studio Code and GitHub Copilot Agent mode.

## 2. Project Objectives

- Understand the fundamentals of Model Context Protocol (MCP).
- Build an MCP server using Python.
- Expose Python functions as MCP tools.
- Configure MCP in Visual Studio Code.
- Connect the server with GitHub Copilot.
- Test MCP tools through Agent mode.

## 3. Technologies Used

| Technology | Purpose |
|---|---|
| Python 3.12 | Programming language |
| MCP Python SDK | MCP server development |
| VS Code | Development environment |
| GitHub Copilot | MCP client |
| PowerShell | Terminal |
| stdio | Communication transport |

## 4. Features

### Tool 1: get_greeting

Accepts a person's name and returns a personalized greeting.

Example:

Input:
```python
name = "Students"
```

Output:
```text
Hello, Students! Your first MCP tool works.
```

### Tool 2: add_numbers

Accepts two integers and returns their sum.

Example:

Input:
```python
a = 10
b = 20
```

Output:
```text
30
```

## 5. Project Structure

```text
hello-mcp/
│
├── server.py
├── requirements.txt
├── README.md
│
├── .venv/
│
└── .vscode/
    └── mcp.json
```

## 6. Installation and Setup

### Prerequisites

- Windows 11
- Python 3.12 or compatible version
- Visual Studio Code
- GitHub Copilot access with Agent mode
- Internet connection

### Step 1: Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd hello-mcp
```

### Step 2: Create a virtual environment

```bash
py -3.12 -m venv .venv
```

### Step 3: Install dependencies

```bash
.venv\Scripts\python.exe -m pip install "mcp[cli]"
```

### Step 4: Run the MCP server

```bash
.venv\Scripts\python.exe server.py
```

Note: The server code and import API must be compatible with the installed MCP SDK version.

## 7. MCP Server Configuration

Create `.vscode/mcp.json`:

```json
{
  "servers": {
    "helloMcp": {
      "type": "stdio",
      "command": "${workspaceFolder}\\.venv\\Scripts\\python.exe",
      "args": ["server.py"]
    }
  }
}
```

## 8. Testing

Use GitHub Copilot Chat in Agent mode.

Test the greeting tool:

```text
Use the get_greeting MCP tool from helloMcp
with the name Students. Show me the result.
```

Test the addition tool:

```text
Use the add_numbers MCP tool from helloMcp
with a = 10 and b = 20. Show me the result.
```

## 9. Expected Results

| MCP Tool | Expected Output |
|---|---|
| get_greeting | Hello, Students! Your first MCP tool works. |
| add_numbers | 30 |

## 10. Learning Outcomes

After completing this project, you will understand:

- MCP architecture and communication.
- Python-based MCP server development.
- Tool registration and execution.
- stdio transport.
- VS Code MCP configuration.
- AI tool integration using GitHub Copilot.

## 11. Future Enhancements

- Add more Python tools.
- Integrate external APIs.
- Connect databases.
- Implement file-processing tools.
- Build more advanced AI-powered MCP applications.

## 12. License

This project is intended for educational and learning purposes. 
