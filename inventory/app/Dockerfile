# Inventory web app + AI tools (Flask, search, updates, optional OpenAI)
FROM python:3.12-slim

WORKDIR /app

# Dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App code (config, routes, updates, flash_ops, project_ops, map_ops, device_ops, debug_ops, config_wizard_ops, device_catalog, static, templates)
COPY config.py app.py updates.py flash_ops.py project_ops.py map_ops.py device_ops.py debug_ops.py config_wizard_ops.py device_catalog.json ./
COPY static/ static/
COPY templates/ templates/

# Default: mount repo at /workspace and set REPO_ROOT
ENV REPO_ROOT=/workspace
ENV PORT=5050
EXPOSE 5050

CMD ["python", "app.py"]
