#!/bin/bash
set -eo pipefail

rm -rf `pwd`/workspace
mkdir -p `pwd`/workspace

pushd agenthub/langchains_gemini_agent
docker build -t control-loop .
popd
docker run \
    -e DEBUG=$DEBUG \
    -e GOOGLE_API_KEY=$GOOGLE_API_KEY \
    -e OPEN_API_KEY="nothing" \
    -u `id -u`:`id -g` \
    -v `pwd`/workspace:/workspace \
    -v `pwd`:/app:ro \
    -e PYTHONPATH=/app \
    control-loop \
    python /app/opendevin/main.py -d /workspace -t "${1}" -c "LangchainsGeminiAgent" -m "gemini-pro"

