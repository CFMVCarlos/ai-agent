<div align="center">

# 🤖 AI Agent

**An autonomous, multi-turn AI coding assistant with tool-calling capabilities, sandboxed workspace operations, and automated code execution.**

[![Python Version](https://img.shields.io/badge/python-3.13%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Package Manager](https://img.shields.io/badge/package_manager-uv-de5fe9.svg?logo=astral&logoColor=white)](https://github.com/astral-sh/uv)
[![Code Style](https://img.shields.io/badge/code%20style-ruff-261230.svg?logo=ruff&logoColor=white)](https://github.com/astral-sh/ruff)
[![Type Checker](https://img.shields.io/badge/type%20checker-basedpyright%20%7C%20ty-brightgreen.svg)](https://github.com/DetachHead/basedpyright)
[![Platform](https://img.shields.io/badge/API-OpenRouter%20%2F%20OpenAI-ff7000.svg)](https://openrouter.ai/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

</div>

---

## 📖 Overview

`aiagent` is an autonomous coding agent written in Python 3.13 using the OpenAI Python SDK and OpenRouter. It leverages native LLM function/tool-calling to inspect codebases, read file contents, write or edit source code, and run Python programs in an isolated working directory. 

With an iterative feedback loop (up to 20 turns per session), the agent plans its actions, executes tools dynamically, inspects runtime outputs or error messages, verifies mathematical calculations, and delivers validated solutions.

---

## ✨ Key Features

- 🔄 **Autonomous Multi-Turn Loop:** Iterates through up to 20 planning-execution turns, calling tools sequentially or in batches and digesting the results before presenting final output.
- 🛠️ **OpenAI Function Calling:** Implements strict `ChatCompletionToolParam` JSON schemas for deterministic tool execution.
- 🛡️ **Path Traversal Protection:** All file system tools restrict access to a designated working directory (`./calculator`), preventing directory traversal outside boundaries.
- ⚡ **Safe Subprocess Execution:** Executes Python scripts via `subprocess.run` with stdout/stderr capture and a 30-second timeout guard.
- 📏 **Truncation & Resource Guarding:** Implements character limits (`MAX_CHARS = 10,000`) to prevent context window overflow when inspecting large files.
- 🧮 **Reasoning & Arithmetic Guidance:** System prompt calibrated for step-by-step mathematical evaluation (operator precedence) and iterative test verification.
- 🔒 **Type-Safe Architecture:** Built with modern Python typing, verified against both `basedpyright` and Astral's `ty` type checker.

---

## 🛠️ Tool Ecosystem

The agent interacts with its workspace through four core tools registered in `functions/call_functions.py`:

| Tool Name | Schema Identifier | Description | Key Parameters |
| :--- | :--- | :--- | :--- |
| **Directory Inspection** | `get_files_info` | Lists files and directories with size in bytes and directory status. | `directory` *(optional, relative)* |
| **File Reader** | `get_file_content` | Reads UTF-8 content up to 10,000 characters with truncation warning. | `file_path` *(required, relative)* |
| **Python Runner** | `run_python_file` | Runs a Python script with optional CLI arguments, capturing stdout/stderr. | `file_path` *(required)*, `args` *(optional)* |
| **File Writer** | `write_file` | Creates parent directories and writes/overwrites file content. | `file_path` *(required)*, `content` *(required)* |

---

## 🏗️ Project Architecture

```
aiagent/
├── calculator/                  # Sandboxed working directory evaluated by the agent
│   ├── pkg/
│   │   ├── calculator.py        # Arithmetic evaluation engine (operator precedence)
│   │   ├── render.py            # JSON output formatter
│   │   └── morelorem.txt        # Test fixture file
│   ├── lorem.backup.txt         # Large test fixture for truncation checks
│   ├── lorem.txt                # Sample text file
│   ├── main.py                  # Calculator CLI entrypoint
│   ├── tests.py                 # Calculator unit test suite
│   └── README.md                # Calculator documentation
├── functions/                   # Agent tool implementations & schemas
│   ├── __init__.py
│   ├── call_functions.py        # Tool registry, schemas, and type-safe dispatcher
│   ├── get_file_content.py      # Bounded file reading utility & schema
│   ├── get_files_info.py        # Directory listing utility & schema
│   ├── run_python_file.py       # Sandboxed script runner & schema
│   └── write_file.py            # Bounded file writing utility & schema
├── config.py                    # Global constants (e.g., MAX_CHARS)
├── main.py                      # Main chatbot CLI & multi-turn execution loop
├── prompts.py                   # System prompt definitions and behavioral rules
├── pyproject.toml               # Project metadata, dependencies, and tool configs
└── uv.lock                      # Locked dependency tree
```

---

## 🚀 Getting Started

### Prerequisites

- [Python 3.13+](https://www.python.org/)
- [`uv`](https://github.com/astral-sh/uv) (recommended) or standard `pip`
- An [OpenRouter](https://openrouter.ai/) API key

### 1. Clone & Install Dependencies

```bash
git clone https://github.com/CFMVCarlos/aiagent.git
cd aiagent

# Install dependencies and sync virtualenv using uv
uv sync
```

### 2. Configure Environment Variables

Create a `.env` file in the root directory:

```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

### 3. Run the Agent

Pass your prompt directly to `main.py`:

```bash
# Basic query
uv run main.py "Inspect the files in the calculator directory and list all tests"

# Verbose mode (displays token usage and function calls in real time)
uv run main.py "Run the calculator tests and fix any failing test cases" --verbose
```

---

## 🧪 Code Quality & Verification Suite

This project adheres to strict quality standards enforced via `uv`:

```bash
# Lint code and apply automatic fixes
uv run ruff check --fix

# Format code
uv run ruff format

# Verify NumPy-style docstrings
uv run pydoclint .

# Fast type check via Astral ty
uv run ty check

# Strict static type check via basedpyright
uv run basedpyright
```

---

## 👤 Author & Acknowledgments

- **Carlos Valente** ([@CFMVCarlos](https://github.com/CFMVCarlos))
- Built as part of the **[Boot.dev](https://boot.dev)** AI Agent engineering curriculum.
