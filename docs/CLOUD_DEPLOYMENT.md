# Cloud Deployment Guide

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
4. **Access**: Your server is available at `https://math-mcp-learning.fastmcp.app/mcp`

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
    # Production FastMCP Cloud URL
    server_url = "https://math-mcp-learning.fastmcp.app/mcp"

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
      "url": "https://math-mcp-learning.fastmcp.app/mcp"
    }
  }
}
```
