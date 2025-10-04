---
name: Strict Git Workflow
description: Enforces feature branch development with mandatory testing and PR reviews for math-mcp-learning-server
---

# Strict Git Workflow Enforcement

## CRITICAL: Pre-Commit Checks (MANDATORY)

Before ANY git commit or push operation, you MUST:

1. **Verify current branch**:
   ```bash
   git branch --show-current
   ```
   - If result is "main" → STOP immediately
   - Create feature branch first: `git checkout -b [type]/[description]`

2. **Run full test suite**:
   ```bash
   uv run pytest tests/ -v      # All tests must pass
   uv run mypy src/             # No type errors
   uv run ruff check            # Linting clean
   ```

3. **Version bump check** (if adding features/fixes):
   - Update `pyproject.toml` version field
   - Semantic versioning: MAJOR.MINOR.PATCH

## Mandatory Workflow (NO EXCEPTIONS)

```bash
# 1. Create feature branch (NEVER work on main)
git checkout -b [type]/[description]
# Types: feature/, fix/, docs/, chore/, enhance/

# 2. Make changes and test FULLY
uv run pytest tests/ -v
uv run mypy src/
uv run ruff check

# 3. Commit to feature branch (NOT main)
git add .
git commit -m "type: clear description"
# NO AI attribution in commits

# 4. Push feature branch
git push -u origin [branch-name]

# 5. Create PR
gh pr create --title "Title" --body "Details..."

# 6. Merge and delete branch
gh pr merge --squash --delete-branch
```

## BLOCKED ACTIONS

You are PROHIBITED from:
- ❌ Running `git commit` while on main branch
- ❌ Running `git push` while on main branch
- ❌ Committing without running tests first
- ❌ Creating commits with AI attribution
- ❌ Merging PRs without deleting feature branch

## Pre-Action Validation

Before executing git commands, ALWAYS:
1. Show current branch: `git branch --show-current`
2. If main → explain you cannot proceed and show correct workflow
3. If feature branch → proceed with workflow steps

## FastMCP Cloud Compatibility

Always use absolute imports (never relative):
```python
# ✅ Correct
from math_mcp import visualization

# ❌ Wrong (breaks FastMCP Cloud)
from . import visualization
```

## Project-Specific Standards

- Version location: `pyproject.toml` line 3
- Test command: `uv run pytest tests/ -v`
- Type checking: `uv run mypy src/`
- Linting: `uv run ruff check`
- Cloud URL: https://math-mcp-learning.fastmcp.app/mcp
- Main branch protection: Enforced via GitHub rulesets

## Error Recovery

If you accidentally attempt to commit to main:
1. GitHub rulesets will block the push
2. Immediately: `git reset --soft HEAD~1`
3. Create feature branch: `git checkout -b fix/description`
4. Follow mandatory workflow above

## Remember

This project uses specialized MCP agents:
- `mcp-specialist`: Architecture review (use first)
- `mcp-coder`: Implementation (use after specialist approval)
- Always: specialist reviews → coder implements

---

*This output style enforces the workflows documented in CLAUDE.md and prevents common git mistakes that have occurred in this project's history.*
