# Contributing to Math MCP Server

Thank you for your interest in contributing to the Math MCP Server! This guide will help you get started and ensure a smooth contribution process.

## 🎯 **Project Philosophy**

This project maintains a **fast & minimal** philosophy while providing educational value:
- ✅ Single-file architecture for core functionality
- ✅ Educational focus on mathematical learning
- ✅ Production-ready security and error handling
- ✅ Comprehensive test coverage
- ❌ Feature bloat or unnecessary complexity

## 🚀 **Quick Start**

### **Prerequisites**
- Python 3.11+
- [uv](https://docs.astral.sh/uv/) package manager
- Git

### **Development Setup**
```bash
# Clone the repository
git clone https://github.com/huguesclouatre/math-mcp-server.git
cd math-mcp-server

# Install dependencies and activate virtual environment
uv sync
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Verify installation
uv run pytest -v
uv run mypy src/
uv run ruff check src/ tests/
```

### **Run the Server**
```bash
# Start the MCP server
uv run python -m math_mcp.server

# Or run directly
uv run src/math_mcp/server.py
```

## 📋 **Development Workflow**

### **Git Workflow**

We use a **feature branch workflow** for substantial changes:

#### **For New Features or Major Changes**
```bash
# 1. Create and switch to feature branch
git checkout -b feature/your-feature-name

# 2. Make your changes
# ... develop, test, commit ...

# 3. Push branch and create PR
git push -u origin feature/your-feature-name
# Visit GitHub to create Pull Request

# 4. After PR approval and merge
git checkout main
git pull origin main
git branch -d feature/your-feature-name
```

#### **For Small Fixes**
```bash
# Direct commits to main are acceptable for:
# - Documentation fixes
# - Typos
# - Minor tweaks
# - Dependency updates

git checkout main
git add .
git commit -m "fix: correct typo in README"
git push origin main
```

### **Commit Message Standards**

We use [Conventional Commits](https://www.conventionalcommits.org/):

```bash
<type>: <description>

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Adding or updating tests
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `chore`: Maintenance tasks

**Examples:**
```bash
feat: add matrix multiplication operations
fix: resolve division by zero error handling
docs: update installation instructions
test: add edge cases for statistical functions
refactor: extract difficulty classification logic
```

## 🧪 **Testing & Quality Assurance**

### **Running Tests**
```bash
# Run all tests
uv run pytest -v

# Run specific test file
uv run pytest tests/test_math_operations.py -v

# Run with coverage
uv run pytest --cov=src --cov-report=html
```

### **Code Quality Checks**
```bash
# Type checking
uv run mypy src/

# Linting and formatting
uv run ruff check src/ tests/
uv run ruff format src/ tests/

# All quality checks at once
uv run pytest -v && uv run mypy src/ && uv run ruff check src/ tests/
```

### **Required Quality Standards**
- ✅ All tests must pass (100% pass rate)
- ✅ Type checking must pass with no errors
- ✅ Linting must pass with no warnings
- ✅ New features require comprehensive tests
- ✅ Security functions must have security tests

## 📝 **Code Standards**

### **Python Style**
- Follow PEP 8 (enforced by ruff)
- Use type hints throughout
- Maximum line length: 88 characters (Black default)
- Use meaningful variable and function names

### **Documentation**
- All functions must have docstrings with examples
- Include parameter descriptions and return types
- Update README.md for user-facing changes
- Add entries to FUTURE_IMPROVEMENTS.md for deferred ideas

### **Security Requirements**
- Never use `eval()` without proper sandboxing
- All user input must be validated
- Log security-relevant events
- Follow principle of least privilege

### **MCP Standards**
- Use FastMCP framework patterns
- Implement proper error handling
- Include educational annotations where appropriate
- Follow MCP protocol specifications

## 🎨 **Architecture Guidelines**

### **File Organization**
```
src/math_mcp/server.py    # Single main file (core principle)
tests/                    # Comprehensive test suite
FUTURE_IMPROVEMENTS.md    # Ideas for later consideration
```

### **Adding New Features**

#### **New Mathematical Operations**
1. Add tool function using `@mcp.tool()` decorator
2. Include comprehensive docstring with examples
3. Add input validation and error handling
4. Include educational annotations
5. Add corresponding tests

#### **New Educational Features**
1. Ensure it serves mathematical learning
2. Keep implementation minimal
3. Add appropriate difficulty classification
4. Test educational metadata

#### **Security Considerations**
- Sanitize all mathematical expressions
- Log suspicious activity
- Validate all inputs
- Test against injection attempts

## 🚀 **Contribution Process**

### **Before You Start**
1. Check existing issues and PRs
2. Review FUTURE_IMPROVEMENTS.md for planned features
3. Discuss major changes in an issue first

### **Making Changes**
1. **Fork the repository** (for external contributors)
2. **Create feature branch** from main
3. **Implement changes** following code standards
4. **Add/update tests** for your changes
5. **Update documentation** as needed
6. **Run quality checks** locally
7. **Commit with conventional messages**

### **Submitting Changes**
1. **Push your branch** to your fork/origin
2. **Create Pull Request** with:
   - Clear title and description
   - Reference any related issues
   - Include testing performed
   - Note any breaking changes

### **PR Review Process**
- Automated checks must pass
- Code review by maintainers
- Discussion of any concerns
- Approval and merge

## 🏷️ **Release Process**

### **Versioning**
We use [Semantic Versioning](https://semver.org/):
- `MAJOR.MINOR.PATCH`
- Major: Breaking changes
- Minor: New features (backward compatible)
- Patch: Bug fixes

### **Release Steps**
```bash
# Tag the release
git tag -a v1.2.0 -m "Add matrix operations and enhanced statistics"
git push origin v1.2.0

# Create GitHub release with changelog
```

## 📚 **Useful Resources**

### **MCP Documentation**
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
- [FastMCP Documentation](https://github.com/modelcontextprotocol/python-sdk)

### **Development Tools**
- [uv Package Manager](https://docs.astral.sh/uv/)
- [Ruff Linter](https://docs.astral.sh/ruff/)
- [mypy Type Checker](https://mypy.readthedocs.io/)

### **Mathematical References**
- [Python Math Module](https://docs.python.org/3/library/math.html)
- [Python Statistics Module](https://docs.python.org/3/library/statistics.html)

## ❓ **Getting Help**

- **Bug Reports**: Open an issue with detailed reproduction steps
- **Feature Requests**: Check FUTURE_IMPROVEMENTS.md first, then open an issue
- **Questions**: Open a discussion or issue
- **Security Issues**: Please report privately to maintainers

## 📄 **Code of Conduct**

- Be respectful and inclusive
- Focus on constructive feedback
- Help maintain a welcoming environment
- Follow the project's educational mission

## 🎯 **What We're Looking For**

### **High Priority Contributions**
- Additional mathematical domains (linear algebra, calculus)
- Educational enhancements (better error explanations)
- Performance improvements
- Security hardening
- Test coverage improvements

### **Medium Priority**
- Documentation improvements
- Example applications
- Integration guides
- Educational use cases

### **Please Avoid**
- Feature bloat that doesn't serve education
- Complex architectural changes without discussion
- Breaking changes without clear benefits
- Dependencies that compromise the minimal philosophy

---

**Thank you for contributing to mathematical education through the MCP protocol!** 🧮✨

For questions about this contributing guide, please open an issue or start a discussion.