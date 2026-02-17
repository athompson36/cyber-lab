# Inventory web app + AI tools (Flask, search, updates, optional OpenAI)
FROM python:3.12-slim

WORKDIR /app

# Dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App code (config, routes, updates, flash_ops, project_ops, static, templates)
COPY config.py app.py updates.py flash_ops.py project_ops.py ./
COPY static/ static/
COPY templates/ templates/

# Default: mount repo at /workspace and set REPO_ROOT
ENV REPO_ROOT=/workspace
ENV PORT=5050
EXPOSE 5050

CMD ["python", "app.py"]
