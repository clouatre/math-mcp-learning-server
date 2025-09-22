# Math MCP Learning Server

[![PyPI version](https://badge.fury.io/py/math-mcp-learning-server.svg)](https://pypi.org/project/math-mcp-learning-server/)

A simple Model Context Protocol (MCP) server for mathematical operations. This project serves as a learning example demonstrating MCP fundamentals and best practices.

## Features

- **Safe Expression Evaluation**: Securely evaluate mathematical expressions with enhanced error handling
- **Educational Annotations**: Responses include difficulty levels and learning metadata
- **Statistical Analysis**: Calculate mean, median, mode, standard deviation, and variance
- **Financial Calculations**: Compound interest calculations with formatted output
- **Unit Conversions**: Length, weight, and temperature conversions
- **Security Logging**: Monitor and log potentially dangerous expression attempts
- **Type Safety**: Full Pydantic validation for inputs and structured content responses
- **Comprehensive Testing**: 100% test pass rate with security and edge case coverage

## Built with MCP Python SDK

This server is built using the official [Model Context Protocol Python SDK](https://github.com/modelcontextprotocol/python-sdk) with FastMCP patterns for rapid development and clean code architecture.

## Available Tools

### 1. `calculate`
Safely evaluate mathematical expressions with support for basic operations and math functions.

**Examples:**
```
2 + 3 * 4          → 14
sqrt(16)          → 4.0
sin(3.14159/2)    → 1.0
abs(-5)           → 5.0
```

### 2. `statistics`
Perform statistical calculations on lists of numbers.

**Operations:** `mean`, `median`, `mode`, `std_dev`, `variance`

**Example:**
```json
{
  "numbers": [1, 2, 3, 4, 5],
  "operation": "mean"
}
```

### 3. `compound_interest`
Calculate compound interest for investments.

**Example:**
```json
{
  "principal": 1000,
  "rate": 0.05,
  "time": 5,
  "compounds_per_year": 12
}
```

### 4. `convert_units`
Convert between different units of measurement.

**Supported unit types:**
- **Length**: mm, cm, m, km, in, ft, yd, mi
- **Weight**: g, kg, oz, lb
- **Temperature**: c, f, k (Celsius, Fahrenheit, Kelvin)

## Installation

### Quick Install from PyPI

The easiest way to use this MCP server is to install it directly from PyPI:

```bash
# Install and run using uvx (recommended)
uvx math-mcp-learning-server

# Or install globally
uv tool install math-mcp-learning-server
```

### Development Setup

For development or to run tests:

```bash
# Clone the repository
git clone https://github.com/huguesclouatre/math-mcp-learning-server.git
cd math-mcp-learning-server

# Install dependencies
uv sync

# Run tests
uv run pytest tests/ -v

# Start the MCP server
uv run math-mcp-learning-server
```

## Development

### Project Structure
```
math-mcp-learning-server/
├── src/math_mcp/
│   ├── __init__.py
│   └── server.py          # Main MCP server implementation
├── tests/
│   └── test_math_operations.py
├── pyproject.toml         # Project configuration
└── README.md
```

### Adding New Tools

1. Define input/output models with Pydantic
2. Add `@mcp.tool()` decorated function
3. Implement tool logic with proper validation
4. Add corresponding tests

### Security Considerations

The `calculate` tool uses restricted `eval()` with:
- Whitelist of allowed characters and functions
- Restricted global scope (only `math` module and `abs`)
- No access to dangerous built-ins or imports

## Usage with Claude Code and Claude Desktop

### Claude Code (Recommended)

Add the MCP server using the Claude Code CLI:

```bash
claude mcp add mathmcp uvx math-mcp-learning-server
```

This automatically configures the server to run from PyPI using uvx.

### Claude Desktop

Add to your Claude Desktop configuration file:

```json
{
  "mcpServers": {
    "math": {
      "command": "uvx",
      "args": ["math-mcp-learning-server"]
    }
  }
}
```

### Development Configuration

For development with local code:

```json
{
  "mcpServers": {
    "math": {
      "command": "uv",
      "args": ["run", "math-mcp-learning-server"],
      "cwd": "/path/to/math-mcp-learning-server"
    }
  }
}
```

## Example Interactions

### Basic Calculation
```
User: Calculate 15% tip on $84.50
Assistant: [uses calculate tool with "84.50 * 0.15"]
Result: 12.675
```

### Statistical Analysis
```
User: What's the average of these test scores: 85, 92, 78, 96, 88?
Assistant: [uses statistics tool with numbers=[85,92,78,96,88], operation="mean"]
Mean: 87.8
```

### Investment Planning
```
User: If I invest $5000 at 4.5% annually, compounded monthly, what will it be worth in 10 years?
Assistant: [uses compound_interest tool]
Principal: $5000.00
Final Amount: $7814.17
Total Interest: $2814.17
```

## Learning Objectives

This project demonstrates:
- MCP protocol implementation with Python
- Safe code execution patterns
- Input validation with Pydantic
- Comprehensive error handling
- Testing strategies for MCP servers
- Professional Python project structure

## Contributing

We welcome contributions! This project follows a **fast & minimal** philosophy while maintaining educational value and professional standards.

**Quick Start for Contributors:**
1. Fork the repository
2. Set up development environment: `uv sync`
3. Create feature branch: `git checkout -b feature/your-feature`
4. Make changes and add tests
5. Run quality checks: `uv run pytest && uv run mypy src/ && uv run ruff check`
6. Submit a pull request

**📋 For detailed guidelines, see [CONTRIBUTING.md](CONTRIBUTING.md)**

Includes:
- Development workflow and Git practices
- Code standards and security requirements
- Testing procedures and quality assurance
- Architecture guidelines and best practices

## Publishing to PyPI

This package is published to PyPI using `uv`. To publish updates:

```bash
# Build the package
uv build

# Publish to PyPI (requires PyPI credentials)
uv publish --token pypi-YOUR_TOKEN_HERE
```

The package follows semantic versioning and includes comprehensive metadata for discoverability on PyPI.

## License

MIT License - see LICENSE file for details

## Next Steps

This basic math MCP can be extended with:
- Matrix operations
- Graphing capabilities
- Advanced statistical functions
- Financial modeling tools
- Integration with external APIs