#!/usr/bin/env python3
"""
Pydantic models for persistent workspace data structures.
Educational MCP server persistence layer models following MCP best practices.
"""

from typing import Any, Dict
from pydantic import BaseModel, Field


class WorkspaceVariable(BaseModel):
    """Persistent workspace variable for cross-session calculations."""

    expression: str = Field(description="The mathematical expression")
    result: float = Field(description="The calculated result")
    timestamp: str = Field(description="When the variable was saved")
    type: str = Field(default="calculation", description="Variable type")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Educational metadata")


class WorkspaceData(BaseModel):
    """Complete workspace data structure for JSON persistence."""

    version: str = Field(default="1.0", description="Schema version")
    created: str = Field(description="Workspace creation timestamp")
    updated: str = Field(description="Last update timestamp")
    variables: Dict[str, WorkspaceVariable] = Field(default_factory=dict, description="Saved calculations")
    statistics: Dict[str, Any] = Field(default_factory=dict, description="Usage statistics")