#!/bin/bash
# Docker build script for voice cloning system

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
IMAGE_NAME="voice-cloning"
IMAGE_TAG="${1:-latest}"
FULL_IMAGE="${IMAGE_NAME}:${IMAGE_TAG}"

echo -e "${GREEN}Building Docker image: ${FULL_IMAGE}${NC}"
echo ""

# Check if NVIDIA Docker runtime is available
if command -v nvidia-docker &> /dev/null || docker run --rm --gpus all nvidia/cuda:12.1.0-base-ubuntu22.04 nvidia-smi &> /dev/null 2>&1; then
    echo -e "${GREEN}✓ NVIDIA Docker runtime detected${NC}"
    GPU_AVAILABLE=true
else
    echo -e "${YELLOW}⚠ NVIDIA Docker runtime not detected${NC}"
    echo -e "${YELLOW}  Image will build but GPU features will be unavailable${NC}"
    GPU_AVAILABLE=false
fi

echo ""
echo "Build configuration:"
echo "  Image name: ${IMAGE_NAME}"
echo "  Image tag: ${IMAGE_TAG}"
echo "  GPU support: ${GPU_AVAILABLE}"
echo ""

# Build the image
echo -e "${GREEN}Starting build...${NC}"
docker build \
    --tag "${FULL_IMAGE}" \
    --build-arg BUILD_DATE="$(date -u +'%Y-%m-%dT%H:%M:%SZ')" \
    --build-arg VCS_REF="$(git rev-parse --short HEAD 2>/dev/null || echo 'unknown')" \
    --build-arg VERSION="${IMAGE_TAG}" \
    .

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✓ Build successful!${NC}"
    echo ""
    echo "Image: ${FULL_IMAGE}"
    echo ""
    echo "Next steps:"
    echo "  • Run web UI:    docker-compose up"
    echo "  • Run CLI:       ./docker-run.sh cli"
    echo "  • Interactive:   ./docker-run.sh shell"
    echo ""
    echo "Push to registry:"
    echo "  • Tag: docker tag ${FULL_IMAGE} your-registry/${FULL_IMAGE}"
    echo "  • Push: docker push your-registry/${FULL_IMAGE}"
    echo ""
else
    echo -e "${RED}✗ Build failed!${NC}"
    exit 1
fi
