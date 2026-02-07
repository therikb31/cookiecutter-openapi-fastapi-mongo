# Use a specialized UV image for faster builds and dependency management
FROM ghcr.io/astral-sh/uv:python{{ cookiecutter.python_version }}-bookworm-slim

WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1
# Ensure the app can find the local packages
ENV PYTHONPATH=/app

# Copy dependency files first for better caching
COPY pyproject.toml README.md ./

# Install dependencies without installing the project itself
RUN uv sync --no-dev

# Copy the library and openapi code required by the service
COPY libs/ ./libs/
COPY openapi/ ./openapi/
# Copy the service code
COPY services/{{ cookiecutter.service_name }}/ ./services/{{ cookiecutter.service_name }}/

# Synchronize the project
RUN uv sync --no-dev

EXPOSE 8000

# Run the service
CMD ["uv", "run", "services/{{ cookiecutter.service_name }}/main.py"]
