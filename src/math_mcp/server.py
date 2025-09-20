#!/usr/bin/env python3
"""
Math MCP Server - FastMCP Implementation
Educational MCP server demonstrating all three MCP pillars: Tools, Resources, and Prompts.
Uses official FastMCP patterns with structured output and multi-transport support.
"""

import math
import statistics
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field
from mcp.server.fastmcp import Context, FastMCP
from mcp.server.session import ServerSession


# === PYDANTIC MODELS FOR STRUCTURED OUTPUT ===

class CalculationResult(BaseModel):
    """Structured result for mathematical calculations."""
    expression: str = Field(description="The original expression")
    result: float = Field(description="The calculated result")
    timestamp: str = Field(description="When the calculation was performed")


class StatisticsResult(BaseModel):
    """Structured result for statistical calculations."""
    operation: str = Field(description="Statistical operation performed")
    input_data: list[float] = Field(description="Input numbers")
    result: float = Field(description="Statistical result")
    count: int = Field(description="Number of data points")


class CompoundInterestResult(BaseModel):
    """Structured result for compound interest calculations."""
    principal: float = Field(description="Initial investment")
    rate: float = Field(description="Annual interest rate")
    time: float = Field(description="Investment period in years")
    compounds_per_year: int = Field(description="Compounding frequency")
    final_amount: float = Field(description="Final amount after compound interest")
    total_interest: float = Field(description="Total interest earned")


class UnitConversionResult(BaseModel):
    """Structured result for unit conversions."""
    original_value: float = Field(description="Original value")
    original_unit: str = Field(description="Original unit")
    converted_value: float = Field(description="Converted value")
    target_unit: str = Field(description="Target unit")
    conversion_type: str = Field(description="Type of conversion")


# === APPLICATION CONTEXT ===

@dataclass
class AppContext:
    """Application context with calculation history."""
    calculation_history: list[dict[str, Any]]


@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    """Manage application lifecycle with calculation history."""
    # Initialize calculation history
    calculation_history: list[dict[str, Any]] = []
    try:
        yield AppContext(calculation_history=calculation_history)
    finally:
        # Could save history to file here
        pass


# === FASTMCP SERVER SETUP ===

mcp = FastMCP(
    name="Math Learning Server",
    lifespan=app_lifespan,
    instructions="A comprehensive math server demonstrating MCP fundamentals with tools, resources, and prompts for educational purposes."
)


# === SECURITY: SAFE EXPRESSION EVALUATION ===

def safe_eval_expression(expression: str) -> float:
    """Safely evaluate mathematical expressions with restricted scope."""
    # Remove whitespace
    clean_expr = expression.replace(" ", "")

    # Only allow safe characters
    allowed_chars = set("0123456789+-*/.()e")
    allowed_functions = {"sin", "cos", "tan", "log", "sqrt", "abs", "pow"}

    # Check for unsafe characters
    if not all(c in allowed_chars or c.isalpha() for c in clean_expr):
        raise ValueError("Expression contains invalid characters")

    # Replace math functions with safe alternatives
    safe_expr = clean_expr
    for func in allowed_functions:
        if func in clean_expr:
            if func != "abs":  # abs is built-in, others need math module
                safe_expr = safe_expr.replace(func, f"math.{func}")

    # Evaluate with restricted globals
    try:
        allowed_globals = {"__builtins__": {"abs": abs}, "math": math}
        result = eval(safe_expr, allowed_globals, {})
        return float(result)
    except Exception as e:
        raise ValueError(f"Invalid expression: {str(e)}")


def convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    """Convert temperature between Celsius, Fahrenheit, and Kelvin."""
    # Convert to Celsius first
    if from_unit.lower() == "f":
        celsius = (value - 32) * 5/9
    elif from_unit.lower() == "k":
        celsius = value - 273.15
    else:  # Celsius
        celsius = value

    # Convert from Celsius to target
    if to_unit.lower() == "f":
        return celsius * 9/5 + 32
    elif to_unit.lower() == "k":
        return celsius + 273.15
    else:  # Celsius
        return celsius


# === TOOLS: COMPUTATIONAL OPERATIONS ===

@mcp.tool()
def calculate(
    expression: str,
    ctx: Context[ServerSession, AppContext]
) -> CalculationResult:
    """Safely evaluate mathematical expressions with support for basic operations and math functions.

    Supported operations: +, -, *, /, **, ()
    Supported functions: sin, cos, tan, log, sqrt, abs, pow

    Examples:
    - "2 + 3 * 4" → 14
    - "sqrt(16)" → 4.0
    - "sin(3.14159/2)" → 1.0
    """
    result = safe_eval_expression(expression)
    timestamp = datetime.now().isoformat()

    # Add to calculation history
    history_entry = {
        "type": "calculation",
        "expression": expression,
        "result": result,
        "timestamp": timestamp
    }
    ctx.request_context.lifespan_context.calculation_history.append(history_entry)

    return CalculationResult(
        expression=expression,
        result=result,
        timestamp=timestamp
    )


@mcp.tool()
def statistics(
    numbers: list[float],
    operation: str
) -> StatisticsResult:
    """Perform statistical calculations on a list of numbers.

    Available operations: mean, median, mode, std_dev, variance
    """
    import statistics as stats  # Import with alias to avoid naming conflict

    if not numbers:
        raise ValueError("Cannot calculate statistics on empty list")

    operations = {
        "mean": stats.mean,
        "median": stats.median,
        "mode": stats.mode,
        "std_dev": lambda x: stats.stdev(x) if len(x) > 1 else 0,
        "variance": lambda x: stats.variance(x) if len(x) > 1 else 0
    }

    if operation not in operations:
        raise ValueError(f"Unknown operation '{operation}'. Available: {list(operations.keys())}")

    result = operations[operation](numbers)

    return StatisticsResult(
        operation=operation,
        input_data=numbers,
        result=result,
        count=len(numbers)
    )


@mcp.tool()
def compound_interest(
    principal: float,
    rate: float,
    time: float,
    compounds_per_year: int = 1
) -> CompoundInterestResult:
    """Calculate compound interest for investments.

    Formula: A = P(1 + r/n)^(nt)
    Where:
    - P = principal amount
    - r = annual interest rate (as decimal)
    - n = number of times interest compounds per year
    - t = time in years
    """
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

    return CompoundInterestResult(
        principal=principal,
        rate=rate,
        time=time,
        compounds_per_year=compounds_per_year,
        final_amount=final_amount,
        total_interest=total_interest
    )


@mcp.tool()
def convert_units(
    value: float,
    from_unit: str,
    to_unit: str,
    unit_type: str
) -> UnitConversionResult:
    """Convert between different units of measurement.

    Supported unit types:
    - length: mm, cm, m, km, in, ft, yd, mi
    - weight: g, kg, oz, lb
    - temperature: c, f, k (Celsius, Fahrenheit, Kelvin)
    """
    # Conversion tables (to base units)
    conversions = {
        "length": {  # to millimeters
            "mm": 1, "cm": 10, "m": 1000, "km": 1000000,
            "in": 25.4, "ft": 304.8, "yd": 914.4, "mi": 1609344
        },
        "weight": {  # to grams
            "g": 1, "kg": 1000, "oz": 28.35, "lb": 453.59
        }
    }

    if unit_type == "temperature":
        result = convert_temperature(value, from_unit, to_unit)
    else:
        conversion_table = conversions.get(unit_type)
        if not conversion_table:
            raise ValueError(f"Unknown unit type '{unit_type}'. Available: length, weight, temperature")

        from_factor = conversion_table.get(from_unit.lower())
        to_factor = conversion_table.get(to_unit.lower())

        if from_factor is None:
            raise ValueError(f"Unknown {unit_type} unit '{from_unit}'")
        if to_factor is None:
            raise ValueError(f"Unknown {unit_type} unit '{to_unit}'")

        # Convert: value → base unit → target unit
        base_value = value * from_factor
        result = base_value / to_factor

    return UnitConversionResult(
        original_value=value,
        original_unit=from_unit,
        converted_value=result,
        target_unit=to_unit,
        conversion_type=unit_type
    )


# === RESOURCES: DATA EXPOSURE ===

@mcp.resource("math://constants/{constant}")
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


@mcp.resource("math://history")
def get_calculation_history(ctx: Context[ServerSession, AppContext]) -> str:
    """Get the history of calculations performed in this session."""
    history = ctx.request_context.lifespan_context.calculation_history

    if not history:
        return "No calculations performed yet in this session."

    history_text = "Calculation History:\n\n"
    for i, entry in enumerate(history[-10:], 1):  # Show last 10
        history_text += f"{i}. {entry['expression']} = {entry['result']} (at {entry['timestamp']})\n"

    if len(history) > 10:
        history_text += f"\n... and {len(history) - 10} more calculations"

    return history_text


# === PROMPTS: INTERACTION TEMPLATES ===

@mcp.prompt()
def math_tutor(
    topic: str,
    level: str = "intermediate",
    include_examples: bool = True
) -> str:
    """Generate a math tutoring prompt for explaining concepts.

    Args:
        topic: Mathematical topic to explain (e.g., "derivatives", "statistics")
        level: Difficulty level (beginner, intermediate, advanced)
        include_examples: Whether to include worked examples
    """
    prompt = f"""You are an expert mathematics tutor. Please explain the concept of {topic} at a {level} level.

Please structure your explanation as follows:
1. **Definition**: Provide a clear, concise definition
2. **Key Concepts**: Break down the main ideas
3. **Applications**: Where this is used in real life
"""

    if include_examples:
        prompt += "4. **Worked Examples**: Provide 2-3 step-by-step examples\n"

    prompt += f"""
Make your explanation engaging and accessible for a {level} learner. Use analogies when helpful, and encourage questions.
"""

    return prompt


@mcp.prompt()
def formula_explainer(
    formula: str,
    context: str = "general mathematics"
) -> str:
    """Generate a prompt for explaining mathematical formulas in detail.

    Args:
        formula: The mathematical formula to explain (e.g., "A = πr²")
        context: The mathematical context (e.g., "geometry", "calculus", "statistics")
    """
    return f"""Please provide a comprehensive explanation of the formula: {formula}

Include the following in your explanation:

1. **What it represents**: What does this formula calculate or describe?
2. **Variable definitions**: Define each variable/symbol in the formula
3. **Context**: How this formula fits within {context}
4. **Step-by-step breakdown**: If the formula has multiple parts, explain each step
5. **Example calculation**: Show how to use the formula with specific numbers
6. **Real-world applications**: Where might someone use this formula?
7. **Common mistakes**: What errors do people often make when using this formula?

Make your explanation clear and educational, suitable for someone learning about {context}.
"""


# === MAIN ENTRY POINT ===

def main():
    """Main entry point supporting multiple transports."""
    import sys

    # Parse command line arguments for transport type
    transport = "stdio"  # default
    if len(sys.argv) > 1:
        if sys.argv[1] in ["stdio", "sse", "streamable-http"]:
            transport = sys.argv[1]

    # Run with specified transport
    mcp.run(transport=transport)


if __name__ == "__main__":
    main()