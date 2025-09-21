# MCP Server Code Review Recommendations

## Overview

Your Math MCP Server demonstrates excellent understanding of MCP fundamentals and follows many SDK best practices. The server is well-architected with proper security, type safety, and comprehensive testing. Below are recommendations for improvements to align with the latest Anthropic MCP Python SDK patterns.

## 1. Server Configuration & Setup

### Use FastMCP High-Level API Consistently

```python
mcp = FastMCP(
    name="Math Learning Server",
    instructions="A comprehensive math server demonstrating MCP fundamentals with tools, resources, and prompts for educational purposes. Supports safe mathematical calculations, statistical analysis, financial computations, and unit conversions.",
    version="0.1.0"
)
```

### Transport Configuration Enhancement

```python
def main():
    import sys
    import argparse

    parser = argparse.ArgumentParser(description="Math MCP Server")
    parser.add_argument("--transport", choices=["stdio", "sse", "streamable-http"],
                       default="stdio", help="Transport type")
    parser.add_argument("--port", type=int, default=8000,
                       help="Port for HTTP transports")
    parser.add_argument("--host", default="localhost",
                       help="Host for HTTP transports")

    args = parser.parse_args()

    # Configure server based on transport
    if args.transport in ["sse", "streamable-http"]:
        mcp.settings.host = args.host
        mcp.settings.port = args.port

    mcp.run(transport=args.transport)
```

## 2. Tool Implementation

### Improve Tool Response Structure

```python
from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent, ToolResult

@mcp.tool()
def calculate(expression: str, ctx: Context[ServerSession, AppContext]) -> ToolResult:
    result = safe_eval_expression(expression)
    timestamp = datetime.now().isoformat()
    difficulty = _classify_expression_difficulty(expression)

    # Add to calculation history
    history_entry = {
        "type": "calculation",
        "expression": expression,
        "result": result,
        "timestamp": timestamp
    }
    ctx.request_context.lifespan_context.calculation_history.append(history_entry)

    return ToolResult(
        content=[
            TextContent(
                type="text",
                text=f"**Calculation:** {expression} = {result}",
                annotations={
                    "difficulty": difficulty,
                    "topic": "arithmetic",
                    "timestamp": timestamp
                }
            )
        ]
    )
```

### Add Tool Input Validation

```python
from pydantic import BaseModel, Field

class CalculateRequest(BaseModel):
    expression: str = Field(..., description="Mathematical expression to evaluate")
    precision: int = Field(default=6, ge=1, le=15, description="Decimal precision for result")

@mcp.tool()
def calculate(request: CalculateRequest, ctx: Context[ServerSession, AppContext]) -> ToolResult:
    result = safe_eval_expression(request.expression)
    # Round to specified precision
    result = round(result, request.precision)
    # ... rest of implementation
```

## 3. Resource Implementation

### Resource URI Pattern Consistency

```python
@mcp.resource("math://v1/constants/{constant}")
def get_math_constant(constant: str) -> str:
    """Get mathematical constants like pi, e, golden ratio, etc."""
    constants = {
        "pi": {"value": math.pi, "description": "Ratio of circle's circumference to diameter"},
        "e": {"value": math.e, "description": "Euler's number, base of natural logarithm"},
        "golden_ratio": {"value": (1 + math.sqrt(5)) / 2, "description": "Golden ratio φ"},
        "euler_gamma": {"value": 0.5772156649015329, "description": "Euler-Mascheroni constant γ"},
        "sqrt2": {"value": math.sqrt(2), "description": "Square root of 2"},
        "sqrt3": {"value": math.sqrt(3), "description": "Square root of 3"}
    }

    if constant not in constants:
        available = ", ".join(constants.keys())
        return f"Unknown constant '{constant}'. Available constants: {available}"

    const_info = constants[constant]
    return f"{constant}: {const_info['value']}\nDescription: {const_info['description']}"
```

### Add Resource Metadata

```python
@mcp.resource("math://constants/{constant}")
def get_math_constant(constant: str) -> str:
    """Get mathematical constants like pi, e, golden ratio, etc."""
    # ... existing logic ...

    # Return structured data instead of plain text
    import json
    return json.dumps({
        "constant": constant,
        "value": const_info['value'],
        "description": const_info['description'],
        "precision": len(str(const_info['value']).split('.')[-1]) if '.' in str(const_info['value']) else 0
    }, indent=2)
```

## 4. Prompt Implementation

### Add Prompt Arguments Validation

```python
from pydantic import BaseModel

class MathTutorRequest(BaseModel):
    topic: str = Field(..., description="Mathematical topic to explain")
    level: str = Field(default="intermediate", enum=["beginner", "intermediate", "advanced"])
    include_examples: bool = Field(default=True, description="Include worked examples")

@mcp.prompt()
def math_tutor(request: MathTutorRequest) -> str:
    """Generate a math tutoring prompt for explaining concepts."""
    prompt = f"""You are an expert mathematics tutor. Please explain the concept of {request.topic} at a {request.level} level.

Please structure your explanation as follows:
1. **Definition**: Provide a clear, concise definition
2. **Key Concepts**: Break down the main ideas
3. **Applications**: Where this is used in real life
"""

    if request.include_examples:
        prompt += "4. **Worked Examples**: Provide 2-3 step-by-step examples\n"

    prompt += f"""
Make your explanation engaging and accessible for a {request.level} learner. Use analogies when helpful, and encourage questions.
"""

    return prompt
```

## 5. Security & Error Handling

### Enhanced Security Logging

```python
import logging
import hashlib

def safe_eval_expression(expression: str) -> float:
    """Safely evaluate mathematical expressions with restricted scope."""
    # Remove whitespace
    clean_expr = expression.replace(" ", "")

    # Only allow safe characters
    allowed_chars = set("0123456789+-*/.()e")
    allowed_functions = {"sin", "cos", "tan", "log", "sqrt", "abs", "pow"}

    # Security check - log and block dangerous patterns
    dangerous_patterns = ["import", "exec", "__", "eval", "open", "file"]
    if any(pattern in clean_expr.lower() for pattern in dangerous_patterns):
        expr_hash = hashlib.sha256(expression.encode()).hexdigest()[:8]
        logging.warning(f"Security: Blocked unsafe expression {expr_hash}: {expression[:50]}...")
        raise ValueError("Expression contains forbidden operations. Only mathematical expressions are allowed.")

    # ... rest of existing implementation
```

### Add Rate Limiting

```python
from collections import defaultdict
import time

class RateLimiter:
    def __init__(self, max_calls: int = 100, window_seconds: int = 60):
        self.max_calls = max_calls
        self.window = window_seconds
        self.calls = defaultdict(list)

    def is_allowed(self, key: str) -> bool:
        now = time.time()
        self.calls[key] = [t for t in self.calls[key] if now - t < self.window]
        if len(self.calls[key]) >= self.max_calls:
            return False
        self.calls[key].append(now)
        return True

# Add to AppContext
@dataclass
class AppContext:
    calculation_history: list[dict[str, Any]]
    rate_limiter: RateLimiter = field(default_factory=RateLimiter)
```

## 6. Lifespan Management

### Add Health Checks and Metrics

```python
@dataclass
class AppContext:
    calculation_history: list[dict[str, Any]]
    start_time: datetime = field(default_factory=datetime.now)
    total_calculations: int = 0

@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    context = AppContext(calculation_history=[])

    # Startup
    logging.info("Math MCP Server starting up")

    try:
        yield context
    finally:
        # Shutdown
        logging.info(f"Math MCP Server shutting down. Total calculations: {context.total_calculations}")
        # Could save metrics here
```

## 7. Testing Improvements

### Add Integration Tests

```python
import pytest
import sys
from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client

@pytest.mark.asyncio
async def test_full_server_integration():
    """Test the complete server with MCP protocol."""
    async with stdio_client([sys.executable, "src/math_mcp/server.py"]) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Test tool listing
            tools = await session.list_tools()
            assert len(tools) == 4  # calculate, statistics, compound_interest, convert_units

            # Test tool call
            result = await session.call_tool("calculate", {"expression": "2 + 3"})
            assert "5.0" in result.content[0].text
```

## 8. Performance & Scalability

### Add Caching for Constants

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_math_constant_cached(constant: str) -> str:
    # ... implementation
```

### Add Async Operations

```python
@mcp.tool()
async def compound_interest(principal: float, rate: float, time: float, compounds_per_year: int = 1) -> ToolResult:
    # Simulate async work (could be database calls, external APIs, etc.)
    await asyncio.sleep(0.01)  # Simulate I/O

    if principal <= 0:
        raise ValueError("Principal must be greater than 0")
    if rate < 0:
        raise ValueError("Interest rate cannot be negative")
    if time <= 0:
        raise ValueError("Time must be greater than 0")
    if compounds_per_year <= 0:
        raise ValueError("Compounds per year must be greater than 0")

    # Calculate compound interest: A = P(1 + r/n)^(nt)
    final_amount = principal * (1 + rate / compounds_per_year) ** (compounds_per_year * time)
    total_interest = final_amount - principal

    return ToolResult(
        content=[
            TextContent(
                type="text",
                text=f"**Compound Interest Calculation:**\nPrincipal: ${principal:,.2f}\nFinal Amount: ${final_amount:,.2f}\nTotal Interest Earned: ${total_interest:,.2f}",
                annotations={
                    "difficulty": "intermediate",
                    "topic": "finance",
                    "formula": "A = P(1 + r/n)^(nt)",
                    "time_years": time
                }
            )
        ]
    )
```

## 9. Documentation & Configuration

### Add Server Metadata

```python
mcp = FastMCP(
    name="Math Learning Server",
    instructions="""A comprehensive math server demonstrating MCP fundamentals.

    Features:
    - Safe mathematical expression evaluation
    - Statistical analysis tools
    - Financial calculations (compound interest)
    - Unit conversion utilities
    - Educational annotations and difficulty levels

    Security: All expressions are evaluated in a restricted environment.""",
    version="0.1.0",
    capabilities={
        "tools": True,
        "resources": True,
        "prompts": True,
        "logging": True
    }
)
```

## Summary

Your MCP server is well-architected and follows many SDK best practices. The main areas for improvement are:

1. **Enhanced type safety** with Pydantic models for all inputs
2. **Better error handling** and security logging
3. **Structured responses** using `ToolResult` and `TextContent`
4. **Rate limiting** and performance optimizations
5. **Integration testing** alongside your excellent unit tests
6. **More comprehensive server metadata** for better AI understanding

The server demonstrates excellent understanding of MCP fundamentals and would benefit most from the structural improvements above to align with the latest SDK patterns.

## Priority Implementation Order

1. **High Priority**: Tool response structure improvements (ToolResult, TextContent)
2. **High Priority**: Enhanced type safety with Pydantic models
3. **Medium Priority**: Security logging enhancements
4. **Medium Priority**: Rate limiting implementation
5. **Low Priority**: Performance optimizations (caching, async operations)
6. **Low Priority**: Integration testing additions

## Testing Recommendations

After implementing changes, ensure:
- All existing unit tests still pass
- New integration tests cover the full MCP protocol flow
- Security tests validate the enhanced logging
- Performance tests confirm no regressions
- Type checking passes with mypy