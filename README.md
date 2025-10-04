# Math MCP Learning Server

[![PyPI version](https://badge.fury.io/py/math-mcp-learning-server.svg)](https://pypi.org/project/math-mcp-learning-server/)

A **persistent quantitative workspace** built as a Model Context Protocol (MCP) server. This project transforms from a basic calculator to provide **cross-session state persistence** - a unique capability that Claude Sonnet 4 cannot achieve natively.

Perfect for learning MCP fundamentals, demonstrating enterprise-grade patterns, and serving as a foundation for advanced mathematical workflows.

## Features

### 🚀 Persistent Workspace (New!)
- **Cross-Session State**: Save calculations and access them across different Claude sessions
- **Persistent Storage**: Variables survive server restarts and session changes
- **Cross-Platform**: Works on Windows (`%LOCALAPPDATA%`), macOS, and Linux (`~/.math-mcp`)
- **Thread-Safe**: Concurrent access with atomic file operations

### 🧮 Mathematical Operations
- **Safe Expression Evaluation**: Securely evaluate mathematical expressions with enhanced error handling
- **Educational Annotations**: Responses include difficulty levels and learning metadata
- **Statistical Analysis**: Calculate mean, median, mode, standard deviation, and variance
- **Financial Calculations**: Compound interest calculations with formatted output
- **Unit Conversions**: Length, weight, and temperature conversions

### 📊 Visual Learning (Optional)
- **Function Plotting**: Generate mathematical function plots with base64-encoded PNG output
- **Statistical Histograms**: Visualize data distributions with mean and median indicators
- **Graceful Degradation**: Optional matplotlib integration with helpful install messages

### 🔒 Enterprise-Grade Quality
- **Security Logging**: Monitor and log potentially dangerous expression attempts
- **Type Safety**: Full Pydantic validation for inputs and structured content responses
- **Comprehensive Testing**: Complete test coverage with security and edge case validation
- **Zero Dependencies**: Core persistence features use only Python stdlib

## Built with FastMCP 2.0

This server is built using [FastMCP 2.0](https://github.com/jlowin/fastmcp) with the official [Model Context Protocol Python SDK](https://github.com/modelcontextprotocol/python-sdk) for rapid development and clean code architecture.

## Available Tools

### 🗄️ Persistent Workspace Tools

#### `save_calculation`
Save calculations to persistent storage for access across sessions.

**Example:**
```json
{
  "name": "portfolio_return",
  "expression": "10000 * 1.07^5",
  "result": 14025.52
}
```

**Use Cases:**
- Save complex financial calculations
- Store frequently used values
- Build persistent calculation workflows

#### `load_variable`
Access previously saved calculations from any Claude session.

**Example:**
```json
{
  "name": "portfolio_return"
}
```
Returns the saved calculation with its expression, result, and metadata.

### 📊 Mathematical Tools

#### `calculate`
Safely evaluate mathematical expressions with support for basic operations and math functions.

**Examples:**
```
2 + 3 * 4          → 14
sqrt(16)           → 4.0
pow(2, 3)          → 8.0
sin(3.14159/2)     → 1.0
abs(-5)            → 5.0
```

#### `statistics`
Perform statistical calculations on lists of numbers.

**Operations:** `mean`, `median`, `mode`, `std_dev`, `variance`

**Example:**
```json
{
  "numbers": [1, 2, 3, 4, 5],
  "operation": "mean"
}
```

#### `compound_interest`
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

#### `convert_units`
Convert between different units of measurement.

**Supported unit types:**
- **Length**: mm, cm, m, km, in, ft, yd, mi
- **Weight**: g, kg, oz, lb
- **Temperature**: c, f, k (Celsius, Fahrenheit, Kelvin)

### 📊 Visualization Tools (Optional)

#### `plot_function`
Generate mathematical function plots for visual learning.

**Example:**
```json
{
  "expression": "x**2",
  "x_range": [-5, 5],
  "num_points": 100
}
```

**Features:**
- Base64-encoded PNG output
- Automatic domain error handling
- Educational annotations
- Grid and axis labels

#### `create_histogram`
Create statistical histograms with distribution analysis.

**Example:**
```json
{
  "data": [1, 2, 2, 3, 3, 3, 4, 4, 5],
  "bins": 5,
  "title": "Test Scores Distribution"
}
```

**Features:**
- Statistical indicators (mean, median)
- Base64-encoded PNG output
- Comprehensive annotations
- Visual data analysis

**Installation for visualization:**
```bash
# Install with plotting support
pip install math-mcp-learning-server[plotting]

# Or for development
uv sync --extra plotting
```

## Available Resources

### `math://workspace`
View your complete persistent workspace with all saved calculations, metadata, and statistics.

**Returns:**
- All saved variables with expressions and results
- Educational metadata (difficulty, topic)
- Workspace statistics (total calculations, session count)
- Timestamps for tracking calculation history

**Example Output:**
```markdown
# Math Workspace (2 variables)

## Saved Variables
- **portfolio_return**: `10000 * 1.07^5` = 14025.52
  - Metadata: difficulty: intermediate, topic: finance
- **circle_area**: `pi * 5^2` = 78.54
  - Metadata: difficulty: basic, topic: geometry

## Statistics
- Total Calculations: 2
- Last Access: 2025-09-28T08:40:34
```

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

## FastMCP Cloud Deployment

Deploy this server to [FastMCP Cloud](https://fastmcp.cloud) for hosted, production-ready access without local setup.

### Deployment Configuration

This server includes a `fastmcp.json` configuration file for seamless cloud deployment:

```json
{
  "source": {
    "type": "filesystem",
    "path": "src/math_mcp/server.py",
    "entrypoint": "mcp"
  },
  "environment": {
    "type": "uv",
    "python": ">=3.11",
    "dependencies": [
      "fastmcp>=2.0.0",
      "pydantic>=2.11.9",
      "matplotlib>=3.8.0",
      "numpy>=1.26.0"
    ]
  },
  "deployment": {
    "transport": "http",
    "log_level": "INFO"
  }
}
```

### Deploy to FastMCP Cloud

1. **Navigate to**: [FastMCP Cloud Dashboard](https://fastmcp.cloud)
2. **Connect GitHub Repository**: `huguesclouatre/math-mcp-learning-server`
3. **Deploy**: FastMCP Cloud auto-detects `fastmcp.json` configuration
4. **Access**: Your server will be available at a provided FastMCP Cloud URL

### Cloud Storage Considerations

**Persistent Workspace Behavior in Cloud:**
- The persistent workspace (`save_calculation`, `load_variable`) uses ephemeral storage in cloud deployments
- Saved calculations persist during active sessions but reset on container restart
- This is standard cloud/serverless behavior and suitable for educational/demonstration purposes

**For production use cases requiring true persistence:**
- Integrate external storage (S3, database, Redis)
- Use environment variables for cloud credentials
- Modify `src/math_mcp/persistence/storage.py` accordingly

### Testing Cloud Deployment

**Using FastMCP Client:**

```python
from fastmcp import Client
import asyncio

async def test_cloud_server():
    # Replace with your actual FastMCP Cloud URL
    server_url = "https://your-server.fastmcp.app/mcp"

    async with Client(server_url) as client:
        # Test calculation
        result = await client.call_tool("calculate", {"expression": "sqrt(16)"})
        print(result)

        # Test statistics
        result = await client.call_tool("statistics", {
            "numbers": [1, 2, 3, 4, 5],
            "operation": "mean"
        })
        print(result)

asyncio.run(test_cloud_server())
```

**Using Claude Desktop:**

Add to your Claude Desktop config:

```json
{
  "mcpServers": {
    "math-learning-cloud": {
      "transport": "http",
      "url": "https://your-server.fastmcp.app/mcp"
    }
  }
}
```

## Development

### Project Structure
```
math-mcp-learning-server/
├── src/math_mcp/
│   ├── __init__.py
│   ├── server.py          # Main MCP server implementation
│   └── persistence/       # Persistent workspace functionality
│       ├── __init__.py
│       ├── models.py      # Pydantic data models
│       ├── storage.py     # Cross-platform file operations
│       └── workspace.py   # Thread-safe workspace manager
├── tests/
│   ├── test_math_operations.py
│   └── test_persistence.py
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

### Persistent Workspace
```
User: Save this portfolio calculation for later: 10000 * 1.07^5
Assistant: [uses save_calculation tool]
Saved Variable: portfolio_return = 14025.52
Expression: 10000 * 1.07^5
Status: Success

User: What was my portfolio return calculation?
Assistant: [uses load_variable tool]
Loaded Variable: portfolio_return = 14025.52
Expression: 10000 * 1.07^5
Saved: 2025-01-15T10:30:00

User: Show me my complete workspace
Assistant: [uses math://workspace resource]
# Math Workspace (2 variables)

## Saved Variables
- portfolio_return: 10000 * 1.07^5 = 14025.52
- circle_area: pi * 5^2 = 78.54

## Statistics
- Total Calculations: 2
- Last Access: 2025-01-15T10:35:00
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

## Code of Conduct

This project adheres to the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to hugues+mcp-coc@linux.com.

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

[MIT License](LICENSE) - Full license details available in the LICENSE file.

## Next Steps

This basic math MCP can be extended with:
- Matrix operations
- Graphing capabilities
- Advanced statistical functions
- Financial modeling tools
- Integration with external APIs