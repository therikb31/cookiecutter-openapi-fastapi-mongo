#!/bin/bash
set -e

if [ -z "$1" ]; then
    echo "Usage: $0 <ServiceName>"
    exit 1
fi

SERVICE_NAME="$1"

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
# Root dir is parent of openapi/ folder
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

INPUT_SPEC="openapi/$SERVICE_NAME/openapi.yaml"
# We output to root and use the relative folder as packageName to ensure correct filesystem alignment
FULL_PACKAGE_NAME="openapi.$SERVICE_NAME"

if [ ! -f "$ROOT_DIR/$INPUT_SPEC" ]; then
    echo "Specification not found at $ROOT_DIR/$INPUT_SPEC" >&2
    exit 1
fi

echo "Generating Python FastAPI models for $SERVICE_NAME with package $FULL_PACKAGE_NAME..."

# Clean up previous generation to remove stale files
GEN_DIR="$ROOT_DIR/openapi/$SERVICE_NAME"
if [ -d "$GEN_DIR/apis" ]; then
    rm -rf "$GEN_DIR/apis"
fi
if [ -d "$GEN_DIR/models" ]; then
    rm -rf "$GEN_DIR/models"
fi

# Run the openapi-generator-cli via Docker
# Note: Ensure the volume mount path is correct for your Docker environment
docker run --rm -v "$ROOT_DIR:/local" openapitools/openapi-generator-cli generate \
    -i "/local/$INPUT_SPEC" \
    -g python-fastapi \
    -o "/local" \
    --global-property "apis,models,supportingFiles,apiTests=false,modelTests=false" \
    --additional-properties="packageName=$FULL_PACKAGE_NAME,sourceFolder=.,skipFormModel=false"

# Ensure all parent directories have __init__.py to be valid packages
CURRENT_PATH="$ROOT_DIR"
PARTS=("openapi" "$SERVICE_NAME")

for PART in "${PARTS[@]}"; do
    CURRENT_PATH="${CURRENT_PATH}/${PART}"
    if [ ! -d "$CURRENT_PATH" ]; then
        mkdir -p "$CURRENT_PATH"
    fi
    if [ ! -f "$CURRENT_PATH/__init__.py" ]; then
        touch "$CURRENT_PATH/__init__.py"
    fi
done

echo "Generation complete. Access via: import $FULL_PACKAGE_NAME"
