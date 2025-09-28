# FastMCP 2.0 Migration Plan

## Overview

This document outlines the migration from FastMCP 1.0 (Official MCP SDK) to FastMCP 2.0 (jlowin/fastmcp) to resolve resource registration issues and enhance the educational MCP server.

## Problem Statement

**Current Issue**: FastMCP 1.0 has confirmed resource registration bugs:
- ✅ Tools work perfectly (`save_calculation`, `load_variable`)
- ✅ Simple parameterized resources work (`math://constants/{constant}`)
- ❌ Complex resources fail (`math://workspace/{view}`, `math://history`)
- ❌ Static resources don't register properly
- ❌ Resources with internal logic fail silently

**Impact**: Phase 1 persistent workspace cannot be browsed as a resource, limiting educational value.

## Solution: FastMCP 2.0 Migration

**Why FastMCP 2.0:**
- Production-ready framework with mature resource handling
- Fixes known resource registration issues
- Better documentation and examples
- Actively maintained with advanced features
- Created by original FastMCP author (Jeff Lowin)

## Migration Scope

### **Version Impact**
- **Current**: 0.2.0 (Phase 1 Complete - FastMCP 1.0)
- **Target**: 0.3.0 (FastMCP 2.0 Migration)
- **Breaking Changes**: Framework dependency change

### **Code Changes Required**
1. **Dependencies**:
   ```diff
   - mcp[server] = "^1.0.0"
   + fastmcp = "^2.0.0"
   ```

2. **Imports**:
   ```diff
   - from mcp.server.fastmcp import FastMCP, Context
   + from fastmcp import FastMCP, Context
   ```

3. **Server Setup**:
   ```diff
   - from mcp.server.session import ServerSession
   + # FastMCP 2.0 handles session management internally
   ```

4. **Resource Patterns**: Update to use FastMCP 2.0 resource registration

### **Testing Strategy**
- **Functional**: All 22 existing tests must pass
- **Resource**: Verify `math://workspace/{view}` and `math://history` work
- **Transport**: Test stdio, SSE, streamable-http transports
- **Persistence**: Ensure workspace compatibility maintained
- **Educational**: Verify learning objectives preserved

## Implementation Timeline

### **Phase 1: Preparation** (Current)
- [x] Document FastMCP 1.0 resource limitation
- [x] Create migration planning document
- [x] Complete current fix branch
- [ ] Push fix branch and merge PR

### **Phase 2: Migration Branch**
- [ ] Create `feature/fastmcp-2.0-migration` branch
- [ ] Update dependencies in pyproject.toml
- [ ] Create backup of working 1.0 version

### **Phase 3: Code Migration**
- [ ] Update server.py imports and patterns
- [ ] Migrate tools (should work as-is)
- [ ] Fix resources with FastMCP 2.0 patterns
- [ ] Update prompts if needed
- [ ] Fix persistence integration

### **Phase 4: Testing & Validation**
- [ ] Run test suite (`uv run pytest tests/ -v`)
- [ ] Test MCP integration manually
- [ ] Verify all resources work
- [ ] Test cross-platform compatibility
- [ ] Performance baseline comparison

### **Phase 5: Documentation & Release**
- [ ] Update README.md with FastMCP 2.0 references
- [ ] Update FUTURE_IMPROVEMENTS.md
- [ ] Create migration guide for users
- [ ] Bump version to 0.3.0
- [ ] Release to PyPI
- [ ] Update CLAUDE.md project standards

## Risk Assessment

### **Low Risk**
- Tools already work perfectly
- Persistence layer is independent
- FastMCP 2.0 designed for compatibility

### **Medium Risk**
- Transport configuration changes
- Context object differences
- Testing framework integration

### **Mitigation Strategies**
- Keep FastMCP 1.0 branch as fallback
- Incremental migration with testing at each step
- Comprehensive test coverage before release

## Success Criteria

### **Functional Requirements**
- [x] All Phase 1 tools work (`save_calculation`, `load_variable`)
- [ ] Resources accessible (`math://workspace/summary`, `math://history`)
- [ ] All 22 tests pass
- [ ] Cross-session persistence maintained
- [ ] Multiple transport support (stdio, SSE, HTTP)

### **Educational Requirements**
- [ ] Clear documentation of MCP concepts
- [ ] Working examples for students
- [ ] Proper error handling and feedback
- [ ] Professional development patterns demonstrated

### **Quality Requirements**
- [ ] Zero functional regressions
- [ ] Improved resource browsing capability
- [ ] Maintained or improved performance
- [ ] Clean migration path documented

## Next Steps

1. **Immediate**: Push current fix branch, create PR, document findings
2. **Short-term**: Create migration branch, begin dependency updates
3. **Medium-term**: Complete migration, comprehensive testing
4. **Long-term**: Release 0.3.0, update educational materials

---

*This migration transforms the Math MCP Learning Server from a demo with resource limitations to a production-ready educational tool with full MCP capability demonstration.*