#!/usr/bin/env sh
uv run uvicorn services.{{ cookiecutter.service_name }}.main:app --host 0.0.0.0 --port 8000
