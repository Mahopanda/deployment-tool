#!/bin/bash

# Check if kustomize and kubectl are installed
command -v kustomize >/dev/null 2>&1 || { echo "kustomize is not installed. Exiting." >&2; exit 1; }
command -v kubectl >/dev/null 2>&1 || { echo "kubectl is not installed. Exiting." >&2; exit 1; }

# Check for environment argument
if [ "$#" -lt 1 ]; then
    echo "Usage: ./deploy.sh [dev|stage|prod] [--dry-run]"
    exit 1
fi

ENV=$1
BASE_DIR="base"
OVERLAYS_DIR="overlays/$ENV"
DRY_RUN=""

if [ "$#" -gt 1 ] && [ "$2" == "--dry-run" ]; then
    DRY_RUN="--dry-run=client -o yaml"
    echo "Running in dry-run mode..."
fi

# Build and apply using kustomize and kubectl
kustomize build $OVERLAYS_DIR | kubectl apply $DRY_RUN -f -

# If dry-run, then also save the combined yaml to a file
if [ ! -z "$DRY_RUN" ]; then
    kustomize build $OVERLAYS_DIR > combined_$ENV.yaml
    echo "Combined YAML has been saved to combined_$ENV.yaml"
fi
