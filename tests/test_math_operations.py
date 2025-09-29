#!/usr/bin/env python3
"""
Test cases for the FastMCP Math Server
"""

import pytest
from math_mcp.server import (
    safe_eval_expression,
    convert_temperature,
    calculate,
    statistics as stats_tool,
    compound_interest,
    convert_units,
    get_math_constant
)


# === SECURITY TESTS ===

def test_safe_eval_basic_operations():
    """Test basic arithmetic operations."""
    assert safe_eval_expression("2 + 3") == 5
    assert safe_eval_expression("10 - 4") == 6
    assert safe_eval_expression("6 * 7") == 42
    assert safe_eval_expression("15 / 3") == 5
    assert safe_eval_expression("2 ** 3") == 8


def test_safe_eval_complex_expressions():
    """Test more complex mathematical expressions."""
    assert safe_eval_expression("2 + 3 * 4") == 14  # Order of operations
    assert safe_eval_expression("(2 + 3) * 4") == 20  # Parentheses
    assert safe_eval_expression("2 ** 3") == 8  # Exponentiation


def test_safe_eval_math_functions():
    """Test mathematical functions."""
    assert abs(safe_eval_expression("sqrt(16)") - 4.0) < 1e-10
    assert abs(safe_eval_expression("abs(-5)") - 5.0) < 1e-10
    assert abs(safe_eval_expression("sin(0)") - 0.0) < 1e-10


def test_safe_eval_invalid_expressions():
    """Test that invalid expressions raise appropriate errors."""
    with pytest.raises(ValueError):
        safe_eval_expression("import os")  # Should be blocked

    with pytest.raises(ValueError):
        safe_eval_expression("__import__('os')")  # Should be blocked

    with pytest.raises(ValueError):
        safe_eval_expression("exec('print(1)')")  # Should be blocked


# === TEMPERATURE CONVERSION TESTS ===

def test_temperature_conversions():
    """Test temperature conversion functions."""
    # Celsius to Fahrenheit
    assert abs(convert_temperature(0, "c", "f") - 32.0) < 1e-10
    assert abs(convert_temperature(100, "c", "f") - 212.0) < 1e-10

    # Fahrenheit to Celsius
    assert abs(convert_temperature(32, "f", "c") - 0.0) < 1e-10
    assert abs(convert_temperature(212, "f", "c") - 100.0) < 1e-10

    # Celsius to Kelvin
    assert abs(convert_temperature(0, "c", "k") - 273.15) < 1e-10


# === FASTMCP TOOL TESTS ===

@pytest.mark.asyncio
async def test_calculate_tool():
    """Test the calculate tool returns structured output with annotations."""
    # Mock context for calculation history
    class MockLifespanContext:
        def __init__(self):
            self.calculation_history = []

    class MockRequestContext:
        def __init__(self):
            self.lifespan_context = MockLifespanContext()

    class MockContext:
        def __init__(self):
            self.request_context = MockRequestContext()
            self.info_logs = []

        async def info(self, message: str):
            """Mock info logging."""
            self.info_logs.append(message)

    ctx = MockContext()
    result = await calculate.fn("2 + 3", ctx)

    assert isinstance(result, dict)
    assert "content" in result
    assert len(result["content"]) == 1
    content = result["content"][0]
    assert content["type"] == "text"
    assert "2 + 3 = 5.0" in content["text"]
    assert "annotations" in content
    assert content["annotations"]["difficulty"] == "basic"
    assert content["annotations"]["topic"] == "arithmetic"


def test_statistics_tool():
    """Test the statistics tool with various operations."""
    # Test mean
    result = stats_tool.fn([1, 2, 3, 4, 5], "mean")
    assert isinstance(result, dict)
    assert "content" in result
    content = result["content"][0]
    assert "Mean" in content["text"]
    assert "3.0" in content["text"]
    assert content["annotations"]["topic"] == "statistics"
    assert content["annotations"]["operation"] == "mean"
    assert content["annotations"]["sample_size"] == 5

    # Test median
    result = stats_tool.fn([1, 2, 3, 4, 5], "median")
    assert "Median" in result["content"][0]["text"]
    assert "3.0" in result["content"][0]["text"]

    # Test empty list
    with pytest.raises(ValueError, match="Cannot calculate statistics on empty list"):
        stats_tool.fn([], "mean")

    # Test invalid operation
    with pytest.raises(ValueError, match="Unknown operation"):
        stats_tool.fn([1, 2, 3], "invalid_op")


def test_compound_interest_tool():
    """Test compound interest calculations."""
    result = compound_interest.fn(1000.0, 0.05, 5.0, 12)

    assert isinstance(result, dict)
    assert "content" in result
    content = result["content"][0]
    assert "Compound Interest Calculation" in content["text"]
    assert "$1,000.00" in content["text"]
    assert content["annotations"]["topic"] == "finance"
    assert content["annotations"]["difficulty"] == "intermediate"
    assert content["annotations"]["time_years"] == 5.0

    # Test validation errors
    with pytest.raises(ValueError, match="Principal must be greater than 0"):
        compound_interest.fn(0, 0.05, 5.0)

    with pytest.raises(ValueError, match="Interest rate cannot be negative"):
        compound_interest.fn(1000, -0.01, 5.0)


def test_convert_units_tool():
    """Test unit conversion tool."""
    # Test length conversion
    result = convert_units.fn(100, "cm", "m", "length")

    assert isinstance(result, dict)
    assert "content" in result
    content = result["content"][0]
    assert "100 cm = 1 m" in content["text"]
    assert content["annotations"]["topic"] == "unit_conversion"
    assert content["annotations"]["conversion_type"] == "length"
    assert content["annotations"]["from_unit"] == "cm"
    assert content["annotations"]["to_unit"] == "m"

    # Test temperature conversion
    result = convert_units.fn(0, "c", "f", "temperature")
    assert "32" in result["content"][0]["text"]

    # Test invalid unit type
    with pytest.raises(ValueError, match="Unknown unit type"):
        convert_units.fn(100, "cm", "m", "invalid_type")


# === RESOURCE TESTS ===

def test_math_constants_resource():
    """Test math constants resource."""
    # Test known constant
    result = get_math_constant.fn("pi")
    assert "pi:" in result
    assert "3.14159" in result
    assert "Description:" in result

    # Test unknown constant
    result = get_math_constant.fn("unknown_constant")
    assert "Unknown constant" in result
    assert "Available constants:" in result


# === INTEGRATION TESTS ===

def test_calculation_with_math_functions():
    """Test calculations that use various math functions."""
    # Test trigonometric functions
    result = safe_eval_expression("sin(0)")
    assert abs(result - 0.0) < 1e-10

    result = safe_eval_expression("cos(0)")
    assert abs(result - 1.0) < 1e-10

    # Test square root
    result = safe_eval_expression("sqrt(25)")
    assert abs(result - 5.0) < 1e-10

    # Test logarithm
    result = safe_eval_expression("log(1)")
    assert abs(result - 0.0) < 1e-10


def test_complex_calculations():
    """Test complex mathematical expressions."""
    # Test compound expression
    result = safe_eval_expression("2 * (3 + 4) - sqrt(16)")
    expected = 2 * (3 + 4) - 4  # 14 - 4 = 10
    assert abs(result - expected) < 1e-10

    # Test with scientific notation
    result = safe_eval_expression("1e2 + 50")
    assert abs(result - 150.0) < 1e-10


def test_statistical_edge_cases():
    """Test statistical functions with edge cases."""
    # Single value
    result = stats_tool.fn([42.0], "mean")
    assert "42.0" in result["content"][0]["text"]

    # Standard deviation with single value
    result = stats_tool.fn([42.0], "std_dev")
    assert "0" in result["content"][0]["text"]  # Should not raise error

    # Variance with single value
    result = stats_tool.fn([42.0], "variance")
    assert "0" in result["content"][0]["text"]  # Should not raise error


def test_unit_conversion_edge_cases():
    """Test unit conversions with various edge cases."""
    # Convert to same unit
    result = convert_units.fn(100, "m", "m", "length")
    assert "100 m = 100 m" in result["content"][0]["text"]

    # Test case insensitivity
    result = convert_units.fn(1, "M", "KM", "length")
    assert "0.001" in result["content"][0]["text"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])