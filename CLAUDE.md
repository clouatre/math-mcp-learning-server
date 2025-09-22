# Math MCP Learning Server - Development Guidelines

## Project-Specific Git Workflow

**CRITICAL: This is an educational MCP server - all changes must follow proper workflow for learning demonstration**

### Mandatory Feature Branch Workflow

```bash
# NEVER do this:
git commit -m "changes" && git push origin main  # ❌ FORBIDDEN

# ALWAYS do this:
git checkout -b feature/descriptive-name         # ✅ REQUIRED
git commit -m "Detailed message"
git push -u origin feature/descriptive-name
gh pr create --title "Clear title" --body "Description"
gh pr merge --squash --delete-branch
```

### Branch Naming Conventions

- **Features**: `feature/persistent-workspace`, `feature/matplotlib-integration`
- **Docs**: `docs/api-validation`, `docs/readme-update`
- **Fixes**: `fix/dependency-patterns`, `fix/security-validation`
- **Enhancement**: `enhance/error-handling`, `enhance/educational-examples`

### Commit Message Examples for This Project

```bash
# ✅ Good examples for this educational MCP:
"Add persistent workspace functionality to enable cross-session calculations"
"Update API recommendations with Context7 validation for educational use"
"Fix MCP dependency patterns to follow official FastMCP guidelines"
"Enhance error messages to provide better learning feedback"

# ❌ Bad examples:
"updates"
"fix stuff"
"changes"
```

### Pull Request Requirements

**Title Format**: `[Type] Clear description of change`
**Examples**:
- `[Feature] Add persistent workspace for cross-session state`
- `[Docs] Update API recommendations with Context7 validation`
- `[Fix] Correct MCP dependency management patterns`

**Body Must Include**:
- **Summary**: What was changed and why
- **Educational Impact**: How this helps MCP learning
- **Testing**: How the change was validated
- **MCP Compliance**: Confirmation of MCP best practices

### Project-Specific Standards

#### MCP Server Development
- **Always validate** against mcp-specialist before major changes
- **Check Context7** for API and library documentation
- **Follow FastMCP patterns** for all server enhancements
- **Maintain educational value** - explain complex concepts clearly

#### Documentation Standards
- **FUTURE_IMPROVEMENTS.md**: Strategic roadmap, requires thorough review
- **README.md**: Installation and usage, keep concise and accurate
- **CONTRIBUTING.md**: Development workflow, update after major pattern changes

#### Testing & Validation
- **Run tests**: `uv run pytest tests/ -v` before committing
- **Check typing**: `uv run mypy src/` for type safety
- **Lint code**: `uv run ruff check` for code quality
- **Security check**: Validate expression evaluation patterns

### Educational Mission Compliance

This project serves as a **learning example** for MCP development:

- **All changes must maintain educational clarity**
- **Code patterns should demonstrate MCP best practices**
- **Documentation must explain "why" not just "what"**
- **Keep the core simple** while adding advanced features as optional enhancements

### Version Management

- **Semantic versioning**: MAJOR.MINOR.PATCH
- **PyPI releases**: Only after thorough testing and documentation updates
- **Git tags**: Create for each PyPI release
- **Changelog**: Update for all user-facing changes

## Emergency Procedures

**If you accidentally commit to main**:
1. Immediately create retroactive feature branch
2. Reset main to previous state
3. Re-commit properly with PR process
4. Document the mistake and correction

**Example recovery**:
```bash
# Reset main (if not pushed to remote yet)
git reset --hard HEAD~1
git checkout -b fix/accidental-main-commit
# Re-apply changes properly
```

---

*This file enforces proper development workflow for the Math MCP Learning Server educational project. All contributors must follow these patterns to maintain code quality and educational value.*