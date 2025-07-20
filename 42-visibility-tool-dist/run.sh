#!/bin/bash
echo "42 Visibility Tool"
if [ -z "$GITHUB_TOKEN" ]; then echo "Error: Set GITHUB_TOKEN first"; exit 1; fi
python3 42-visibility-tool.py
