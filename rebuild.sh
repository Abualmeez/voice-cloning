#!/bin/bash
# Quick rebuild script - removes old image and builds fresh

set -e

echo "🔨 Rebuilding Docker image with fixed dependencies..."
echo ""

# Stop any running containers
echo "Stopping running containers..."
sudo docker stop voice-cloning-app 2>/dev/null || true

# Remove old image to force complete rebuild
echo "Removing old image..."
sudo docker rmi voice-cloning:latest 2>/dev/null || true

# Build fresh image
echo ""
echo "Building new image..."
sudo docker build --no-cache -t voice-cloning:latest .

echo ""
echo "✅ Rebuild complete!"
echo ""
echo "Run: sudo ./docker-run.sh web"
