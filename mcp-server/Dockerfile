# ESP32 Lab MCP Server — project context, roadmap, devices, inventory
# Run with repo mounted at /workspace so the server can read repo files.
# Cursor: docker run --rm -i -v "$(pwd)":/workspace -e ESP32_LAB_REPO_ROOT=/workspace esp32-lab-mcp

FROM node:20-slim

WORKDIR /app

# Install deps (include dev for TypeScript) and build
COPY package.json package-lock.json* ./
RUN npm ci
COPY tsconfig.json ./
COPY src/ src/
RUN npm run build

# Server reads from REPO_ROOT (mount at runtime)
ENV ESP32_LAB_REPO_ROOT=/workspace

# Stdio transport: no port, client talks over stdin/stdout
CMD ["node", "dist/index.js"]
