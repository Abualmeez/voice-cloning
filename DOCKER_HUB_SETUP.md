# Docker Hub & GitHub Setup Guide

Complete guide for publishing your voice cloning system to Docker Hub and GitHub.

## Prerequisites

- Docker Hub account
- GitHub account
- Git installed locally
- Docker and Docker Compose installed

## Step 1: Create Docker Hub Account

1. Go to https://hub.docker.com
2. Sign up for a free account
3. Note your username (e.g., `johndoe`)

### Create Access Token

1. Log in to Docker Hub
2. Go to Account Settings → Security
3. Click "New Access Token"
4. Name: `github-actions`
5. Permissions: Read, Write, Delete
6. Copy the token (you'll only see it once!)

## Step 2: Setup GitHub Repository

### Create Repository

1. Go to https://github.com
2. Click "New repository"
3. Name: `voice-cloning`
4. Description: `Local AI voice cloning with Coqui TTS XTTS-v2`
5. Choose Public or Private
6. Don't initialize with README (we already have one)
7. Click "Create repository"

### Add GitHub Secrets

1. Go to your repository Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Add these secrets:

**DOCKERHUB_USERNAME**
- Name: `DOCKERHUB_USERNAME`
- Secret: Your Docker Hub username (e.g., `johndoe`)

**DOCKERHUB_TOKEN**
- Name: `DOCKERHUB_TOKEN`
- Secret: The access token you copied from Docker Hub

## Step 3: Initialize Git Repository

```bash
cd voice-cloning

# Initialize git (if not already done)
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Voice cloning system with Docker support"

# Add remote (replace with your username)
git remote add origin https://github.com/adakrupp/voice-cloning.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 4: Verify GitHub Actions

1. Go to your GitHub repository
2. Click the "Actions" tab
3. You should see the "Build and Publish Docker Image" workflow running
4. Wait for it to complete (may take 10-15 minutes for first build)

Once complete, your image will be available at:
- Docker Hub: `https://hub.docker.com/r/adakrupp/voice-cloning`
- GitHub Packages: `ghcr.io/adakrupp/voice-cloning`

## Step 5: Test Pulling the Image

```bash
# Pull from Docker Hub
docker pull adakrupp/voice-cloning:latest

# Run the web UI
docker run --rm -it --gpus all \
  -p 7860:7860 \
  -v $(pwd)/voices:/app/voices \
  -v $(pwd)/outputs:/app/outputs \
  adakrupp/voice-cloning:latest \
  python3 web_ui.py --host 0.0.0.0
```

Access at: http://localhost:7860

## Step 6: Update Docker Compose for Public Image

Edit `docker-compose.yml` to use your published image:

```yaml
services:
  voice-cloning:
    image: adakrupp/voice-cloning:latest
    # Remove the 'build' section if you want to use pre-built image
```

## Publishing New Versions

### Automatic (Recommended)

GitHub Actions automatically builds on every push:

```bash
# Make changes
git add .
git commit -m "Add new feature"
git push

# Wait for GitHub Actions to build and push
```

### Tagged Releases

Create version tags for releases:

```bash
# Tag a release
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0

# This creates tags on Docker Hub:
# - adakrupp/voice-cloning:v1.0.0
# - adakrupp/voice-cloning:1.0
# - adakrupp/voice-cloning:1
```

### Manual Push

```bash
# Build locally
./docker-build.sh v1.0.0

# Login to Docker Hub
docker login

# Tag image
docker tag voice-cloning:v1.0.0 adakrupp/voice-cloning:v1.0.0
docker tag voice-cloning:v1.0.0 adakrupp/voice-cloning:latest

# Push to Docker Hub
docker push adakrupp/voice-cloning:v1.0.0
docker push adakrupp/voice-cloning:latest
```

## Updating Docker Hub Description

The GitHub Actions workflow automatically updates your Docker Hub repository description from `README.md`.

To manually update:

```bash
# Install docker-pushrm
wget https://github.com/christian-korneck/docker-pushrm/releases/download/v1.9.0/docker-pushrm_linux_amd64
chmod +x docker-pushrm_linux_amd64
sudo mv docker-pushrm_linux_amd64 /usr/local/bin/docker-pushrm

# Push README to Docker Hub
docker-pushrm adakrupp/voice-cloning
```

## Customizing the Build

### Build Arguments

Edit `.github/workflows/docker-publish.yml` to add custom build args:

```yaml
build-args: |
  BUILD_DATE=${{ github.event.repository.updated_at }}
  VCS_REF=${{ github.sha }}
  VERSION=${{ steps.meta.outputs.version }}
  CUSTOM_ARG=value
```

### Multi-Platform Builds

To build for multiple architectures (e.g., ARM64):

Edit `docker-publish.yml`:

```yaml
env:
  DOCKER_PLATFORMS: linux/amd64,linux/arm64
```

**Note:** ARM64 builds are slower and may require emulation.

## Monitoring and Maintenance

### View Build Status

- GitHub: https://github.com/adakrupp/voice-cloning/actions
- Badge: Add to README.md:

```markdown
![Docker Build](https://github.com/adakrupp/voice-cloning/workflows/Build%20and%20Publish%20Docker%20Image/badge.svg)
```

### Docker Hub Stats

Check your Docker Hub repository for:
- Pull statistics
- Stars/favorites
- Tags and versions

### Cleanup Old Images

```bash
# List all tags
docker images adakrupp/voice-cloning

# Remove old tags
docker rmi adakrupp/voice-cloning:old-tag
```

## Troubleshooting

### GitHub Actions Fails

**Check secrets:**
```bash
# Verify secrets are set in Settings → Secrets and variables → Actions
```

**View logs:**
1. Go to Actions tab
2. Click the failed workflow
3. Expand failed step to see error

### Docker Push Permission Denied

```bash
# Re-login to Docker Hub
docker logout
docker login

# Verify token has write permissions
```

### Image Size Too Large

```bash
# Check image size
docker images adakrupp/voice-cloning

# If > 5GB, consider:
# - Using multi-stage builds
# - Removing unnecessary dependencies
# - Compressing layers
```

### Build Timeout

Free GitHub Actions has 6-hour limit. If builds timeout:
- Use Docker Hub automated builds instead
- Upgrade to GitHub Actions paid plan
- Build locally and push manually

## Security Best Practices

1. **Never commit tokens** - Use GitHub secrets only
2. **Rotate tokens** - Change Docker Hub token annually
3. **Limit permissions** - Token should only have needed permissions
4. **Review pull requests** - Don't auto-build from untrusted PRs
5. **Scan images** - Enable Docker Hub vulnerability scanning

## Additional Resources

- Docker Hub Docs: https://docs.docker.com/docker-hub/
- GitHub Actions Docs: https://docs.github.com/en/actions
- Docker Build Docs: https://docs.docker.com/build/
- Container Security: https://docs.docker.com/engine/security/

## Support

For issues:
1. Check GitHub Actions logs
2. Review Docker build output
3. Test locally first: `./docker-build.sh`
4. Create issue on GitHub repository

---

**Your image will be available at:**
- `docker pull adakrupp/voice-cloning:latest`
- `https://hub.docker.com/r/adakrupp/voice-cloning`
