Name: Sumana Sri
Roll No: 261FB04017

# 1. Project Title

**Hello MCP – Python Model Context Protocol Server**

---

## 2. Project Overview

**Hello MCP** (`hello-mcp`) is a local Model Context Protocol (MCP) server implemented in Python 3.12 using the official Python MCP SDK (`mcp==2.3.0` with CLI extras). The server exposes deterministic Python functions as structured MCP tools over standard input/output (`stdio`) transport so that an MCP-capable client—specifically Visual Studio Code with GitHub Copilot Agent Mode—can discover, validate, and invoke them at runtime.

---

## 3. Problem Statement and Objectives

### Problem Statement
Large Language Model (LLM) assistants operating inside an IDE require a standardized, secure, and transport-agnostic protocol to invoke external deterministic functions without custom integration glue code for each tool or host environment.

### Objectives
1. Provision an isolated Python 3.12 virtual environment (`.venv`) containing the MCP Python SDK (`mcp[cli]` v2.x).
2. Implement a standards-compliant MCP server (`server.py`) named `"Hello MCP"` using `MCPServer` from `mcp.server.mcpserver`.
3. Register two strongly typed MCP tools:
   - `get_greeting(name: str) -> str`: Returns a personalized greeting string for a student.
   - `add_numbers(a: int, b: int) -> int`: Computes and returns the integer sum of two integers.
4. Configure VS Code workspace MCP discovery (`.vscode/mcp.json`) using portable workspace variables (`${workspaceFolder}`) and `stdio` transport.
5. Verify server initialization, JSON Schema tool discovery, and end-to-end tool execution against the specification in `Python_MCP_Server_Detailed_Guide.pdf`.

---

## 4. Technology Stack

| Component | Technology / Version | Purpose |
| :--- | :--- | :--- |
| **Operating System** | Windows 10/11 (64-bit) | Host execution environment |
| **Programming Language** | Python `3.12.10` | Runtime interpreter for the MCP server |
| **Environment Isolation** | Python `venv` (`.venv`) | Project-scoped package isolation |
| **MCP SDK** | `mcp==2.3.0` (`mcp[cli]`), `mcp-types==2.3.0` | Model Context Protocol server framework & CLI extras |
| **Schema & Validation** | `pydantic==2.14.3`, `jsonschema==4.26.0` | Automatic tool input/output JSON Schema generation and validation |
| **Async Runtime** | `anyio==4.16.0` | Asynchronous `stdio` stream management |
| **Transport Protocol** | JSON-RPC 2.0 over `stdio` | Standard input/output communication between client and server |
| **Client / IDE** | Visual Studio Code + GitHub Copilot Agent Mode | MCP host and client discovering and calling registered tools |

---

## 5. System Architecture Diagram

```text
+-------------------------------------------------------------------+
|             Visual Studio Code (GitHub Copilot Agent Mode)        |
|  - Reads .vscode/mcp.json ("helloMcp" configuration)              |
|  - Launches .venv\Scripts\python.exe server.py                    |
+-------------------------------------------------------------------+
                                 |  ^
      JSON-RPC 2.0 Requests      |  |      JSON-RPC 2.0 Responses
   (initialize, tools/list,      |  |   (Server capabilities, tool
         tools/call)             |  |    schemas, execution results)
                                 v  |
                         [ stdio transport ]
                                 |  ^
                                 v  |
+-------------------------------------------------------------------+
|               Hello MCP Server (server.py in .venv)               |
|  - Instance: MCPServer("Hello MCP")                               |
|                                                                   |
|  +-------------------------------------------------------------+  |
|  | @mcp.tool()                                                 |  |
|  | get_greeting(name: str) -> str                              |  |
|  | Returns: f"Hello, {name}! Your first MCP tool works."       |  |
|  +-------------------------------------------------------------+  |
|                                                                   |
|  +-------------------------------------------------------------+  |
|  | @mcp.tool()                                                 |  |
|  | add_numbers(a: int, b: int) -> int                          |  |
|  | Returns: a + b                                              |  |
|  +-------------------------------------------------------------+  |
+-------------------------------------------------------------------+
```

---

## 6. Project Directory Structure

```text
hello-mcp/
│
├── .venv/
│
├── .vscode/
│   └── mcp.json
│
├── server.py
│
├── requirements.txt
│
└── README.md
```

- **`.venv/`**: Isolated Python 3.12 virtual environment containing `.venv\Scripts\python.exe` and `mcp==2.3.0`.
- **`.vscode/mcp.json`**: Workspace-level VS Code MCP configuration defining how to launch `helloMcp` over `stdio`.
- **`server.py`**: Core Python MCP server implementation defining and exposing `get_greeting` and `add_numbers`.
- **`requirements.txt`**: UTF-8 encoded dependency manifest recording all 38 pinned packages installed in `.venv`.
- **`README.md`**: Complete academic and technical documentation for the project.

---

## 7. Explanation of `server.py`

```python
from mcp.server.mcpserver import MCPServer
mcp = MCPServer("Hello MCP")

@mcp.tool()
def get_greeting(name: str) -> str:
    """Return a greeting for a student."""
    return f"Hello, {name}! Your first MCP tool works."

@mcp.tool()
def add_numbers(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

if __name__ == "__main__":
    mcp.run()
```

### Line-by-Line Breakdown
1. **`from mcp.server.mcpserver import MCPServer`**: Imports the high-level `MCPServer` class provided by the MCP Python SDK (`mcp==2.3.0`).
2. **`mcp = MCPServer("Hello MCP")`**: Instantiates the MCP server and assigns its protocol-visible server name (`"Hello MCP"`).
3. **`@mcp.tool()`**: Decorator that registers the decorated Python function in the server's tool registry, introspecting its function name, docstring, and type annotations to generate an MCP-compliant JSON Schema.
4. **`if __name__ == "__main__": mcp.run()`**: Starts the MCP server event loop when `server.py` is executed directly. By default, `mcp.run()` uses `transport="stdio"`.

---

## 8. Explanation of Both MCP Tools

### Tool 1: `get_greeting`
- **Signature:** `get_greeting(name: str) -> str`
- **Description:** `"Return a greeting for a student."`
- **Input Schema:**
  ```json
  {
    "title": "get_greetingArguments",
    "type": "object",
    "properties": {
      "name": {
        "title": "Name",
        "type": "string"
      }
    },
    "required": ["name"]
  }
  ```
- **Behavior:** Accepts a required string argument `name` and returns the formatted string `f"Hello, {name}! Your first MCP tool works."`.

### Tool 2: `add_numbers`
- **Signature:** `add_numbers(a: int, b: int) -> int`
- **Description:** `"Add two numbers."`
- **Input Schema:**
  ```json
  {
    "title": "add_numbersArguments",
    "type": "object",
    "properties": {
      "a": {
        "title": "A",
        "type": "integer"
      },
      "b": {
        "title": "B",
        "type": "integer"
      }
    },
    "required": ["a", "b"]
  }
  ```
- **Behavior:** Accepts two required integer arguments `a` and `b` and returns their arithmetic sum `a + b`.

---

## 9. Python Environment Setup

1. Verify that Python 3.12 or above is available via the Windows Python launcher:
   ```cmd
   py --version
   py -0p
   ```
2. Create the project directory and navigate into it:
   ```cmd
   mkdir hello-mcp
   cd hello-mcp
   ```
3. Create the isolated virtual environment (`.venv`) using Python 3.12:
   ```cmd
   py -3.12 -m venv .venv
   ```
4. Confirm that `.venv\Scripts\python.exe` exists:
   ```cmd
   dir .venv\Scripts
   .venv\Scripts\python.exe --version
   ```

---

## 10. Installation Instructions

Install the MCP Python SDK with CLI extras inside the project's virtual environment:

```cmd
.venv\Scripts\python.exe -m pip install "mcp[cli]" --default-timeout=120
```

Alternatively, reproduce the exact pinned environment from `requirements.txt`:

```cmd
.venv\Scripts\python.exe -m pip install -r requirements.txt --default-timeout=120
```

Verify the installed `mcp` package metadata and record dependencies:

```cmd
.venv\Scripts\python.exe -m pip show mcp
```

---

## 11. MCP Configuration

The workspace MCP configuration is stored in `.vscode/mcp.json`:

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

### Configuration Parameters
- **`helloMcp`**: Unique identifier for this MCP server in VS Code.
- **`type: "stdio"`**: Configures standard input/output transport between the client and the spawned Python process.
- **`command`**: Uses `${workspaceFolder}\\.venv\\Scripts\\python.exe` so the configuration is portable across machines and always runs inside the project's virtual environment.
- **`args`**: Passes `["server.py"]` as the entrypoint script executed by the Python interpreter.

---

## 12. Execution Instructions

### Starting / Restarting the Server in VS Code
1. Save both `server.py` and `.vscode/mcp.json`.
2. Press `Ctrl + Shift + P` in VS Code to open the Command Palette.
3. Type and select **`MCP: List Servers`**.
4. Select **`helloMcp`** from the server list and choose **Start** (or **Restart**).
5. Confirm that the server status transitions to **Running / Connected** and reports **2 tools discovered** (`get_greeting` and `add_numbers`).

---

## 13. Testing Procedures

### Method 1: Testing through GitHub Copilot Agent Mode (VS Code UI)
Open GitHub Copilot Chat in VS Code, switch the mode selector to **Agent**, and execute the following test prompts:

- **Test A (`get_greeting`):**
  ```text
  Use the get_greeting MCP tool from helloMcp with the name Students. Show me the result.
  ```
- **Test B (`add_numbers`):**
  ```text
  Use the add_numbers MCP tool from helloMcp with a = 10 and b = 20. Show me the result.
  ```

### Method 2: Programmatic Verification (Direct Function & End-to-End `stdio` Protocol Client)
Run the virtual environment interpreter to verify direct tool invocation and full JSON-RPC `stdio` client-server protocol handshake (`initialize`, `tools/list`, and `tools/call`):

```cmd
.venv\Scripts\python.exe -B -c "import server; print(server.get_greeting(name='Students')); print(server.add_numbers(a=10, b=20))"
```

---

## 14. Actual Successful Test Outputs

The following outputs were captured directly from the project's `.venv` environment (`Python 3.12.10`, `mcp==2.3.0`):

### Environment & Package Verification Output
```text
Python 3.12.10
Name: mcp
Version: 2.3.0
Summary: Model Context Protocol SDK
Home-page: https://modelcontextprotocol.io
Author: Model Context Protocol a Series of LF Projects, LLC.
License: MIT
Requires: anyio, httpx2, jsonschema, mcp-types, opentelemetry-api, pydantic, pyjwt, python-multipart, pywin32, sse-starlette, starlette, typing-extensions, typing-inspection, uvicorn
```

### Direct Tool Invocation Output
```text
get_greeting(name='Students') -> 'Hello, Students! Your first MCP tool works.'
add_numbers(a=10, b=20)       -> 30
```

### End-to-End MCP `stdio` Client-Server Protocol Test Output
```text
INITIALIZE: name='Hello MCP' title=None version='' description=None website_url=None icons=None
TOOLS DISCOVERED: 2
  1. get_greeting: Return a greeting for a student.
     Schema: {'properties': {'name': {'title': 'Name', 'type': 'string'}}, 'required': ['name'], 'type': 'object', 'title': 'get_greetingArguments'}
  2. add_numbers: Add two numbers.
     Schema: {'properties': {'a': {'title': 'A', 'type': 'integer'}, 'b': {'title': 'B', 'type': 'integer'}}, 'required': ['a', 'b'], 'type': 'object', 'title': 'add_numbersArguments'}
CALL get_greeting(name='Students'): Hello, Students! Your first MCP tool works.
CALL add_numbers(a=10, b=20): 30
```

---

## 15. Expected Results

| Test Case | Tool Name | Input Arguments | Expected Output | Verified Output |
| :--- | :--- | :--- | :--- | :--- |
| **Test 1** | `get_greeting` | `name = "Students"` | `Hello, Students! Your first MCP tool works.` | `Hello, Students! Your first MCP tool works.` |
| **Test 2** | `add_numbers` | `a = 10, b = 20` | `30` | `30` |

---

## 16. Learning Outcomes

1. **Model Context Protocol Fundamentals:** Understood how MCP decouples LLM hosts/clients from local tool servers using JSON-RPC 2.0 messages over `stdio`.
2. **SDK 2.x Server Authoring:** Learned how to instantiate `MCPServer` from `mcp.server.mcpserver` and expose strongly typed Python functions via the `@mcp.tool()` decorator.
3. **Automatic Schema Introspection:** Observed how Python type annotations (`str`, `int`) and docstrings are converted into JSON Schema definitions for client-side tool discovery and argument validation.
4. **Portable IDE Integration:** Learned how to configure `.vscode/mcp.json` using `${workspaceFolder}` and virtual environment executables so projects remain portable across machines.
5. **Reproducible Python Environments:** Practiced isolating dependencies inside `.venv` and recording UTF-8 package manifests in `requirements.txt`.

---

## 17. Conclusion

The **Hello MCP** server project fulfills the technical requirements of `Python_MCP_Server_Detailed_Guide.pdf`. Running on Python `3.12.10` with `mcp==2.3.0` inside an isolated virtual environment, `server.py` accurately exposes `get_greeting` and `add_numbers` over `stdio`, `.vscode/mcp.json` provides a portable VS Code client configuration, `requirements.txt` records all pinned dependencies in standard UTF-8 format, and end-to-end `stdio` protocol testing confirms error-free initialization, tool discovery, and tool execution.
