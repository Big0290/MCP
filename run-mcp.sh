#!/bin/bash

# Run the MCP server in the container with stdin/stdout communication
docker exec -i mcp-project-server uv run main.py
