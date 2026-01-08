#!/bin/bash
# Docker run script for voice cloning system

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Configuration
IMAGE_NAME="voice-cloning:latest"
CONTAINER_NAME="voice-cloning-app"

# Parse command
COMMAND="${1:-web}"

# GPU support
GPU_FLAGS="--gpus all"
if ! docker run --rm --gpus all nvidia/cuda:12.1.0-base-ubuntu22.04 nvidia-smi &> /dev/null 2>&1; then
    echo -e "${YELLOW}⚠ GPU not available, running in CPU mode${NC}"
    GPU_FLAGS=""
fi

# Common docker run options
DOCKER_OPTS="
    --rm
    -it
    ${GPU_FLAGS}
    --name ${CONTAINER_NAME}
    -v $(pwd)/voices:/app/voices
    -v $(pwd)/outputs:/app/outputs
    -v $(pwd)/models:/app/models
"

case "$COMMAND" in
    web)
        echo -e "${GREEN}Starting web UI...${NC}"
        echo "Access at: http://localhost:7860"
        echo ""
        echo -e "${YELLOW}⚠️  WARNING: Web UI will be accessible from all network interfaces${NC}"
        echo "   For production use, add authentication or bind to localhost only"
        echo "   Example: python3 web_ui.py --host 127.0.0.1 --auth admin password"
        echo ""
        docker run ${DOCKER_OPTS} \
            -p 7860:7860 \
            ${IMAGE_NAME} \
            python3 web_ui.py --host 0.0.0.0 --port 7860
        ;;

    cli)
        echo -e "${GREEN}Starting interactive CLI...${NC}"
        docker run ${DOCKER_OPTS} \
            ${IMAGE_NAME} \
            python3 cli.py --interactive
        ;;

    record)
        echo -e "${GREEN}Starting voice recording...${NC}"
        DURATION="${2:-120}"
        docker run ${DOCKER_OPTS} \
            --device /dev/snd \
            ${IMAGE_NAME} \
            python3 scripts/record_voice.py ${DURATION}
        ;;

    prepare)
        echo -e "${GREEN}Preparing audio files...${NC}"
        docker run ${DOCKER_OPTS} \
            ${IMAGE_NAME} \
            python3 scripts/prepare_audio.py
        ;;

    clone)
        if [ -z "$2" ]; then
            echo "Usage: $0 clone \"Your text here\""
            exit 1
        fi
        echo -e "${GREEN}Generating speech...${NC}"
        docker run ${DOCKER_OPTS} \
            ${IMAGE_NAME} \
            python3 quick_clone.py "$2"
        ;;

    shell)
        echo -e "${GREEN}Starting interactive shell...${NC}"
        docker run ${DOCKER_OPTS} \
            ${IMAGE_NAME} \
            /bin/bash
        ;;

    help)
        echo "Voice Cloning Docker Runner"
        echo ""
        echo "Usage: $0 <command> [options]"
        echo ""
        echo "Commands:"
        echo "  web              Start web UI (default, port 7860)"
        echo "  cli              Start interactive CLI"
        echo "  record [secs]    Record voice (default: 120 seconds)"
        echo "  prepare          Prepare recorded audio"
        echo "  clone \"text\"     Generate speech from text"
        echo "  shell            Start bash shell"
        echo "  help             Show this help"
        echo ""
        echo "Examples:"
        echo "  $0 web"
        echo "  $0 cli"
        echo "  $0 record 60"
        echo "  $0 clone \"Hello world!\""
        echo ""
        ;;

    *)
        echo "Unknown command: $COMMAND"
        echo "Run '$0 help' for usage"
        exit 1
        ;;
esac
