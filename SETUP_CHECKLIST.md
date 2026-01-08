# Setup Checklist

Complete checklist for deploying the Voice Cloning System to Docker Hub and GitHub.

## Pre-Deployment Checklist

### Local Testing

- [ ] Test Docker build locally: `./docker-build.sh`
- [ ] Test web UI: `./docker-run.sh web`
- [ ] Test CLI: `./docker-run.sh cli`
- [ ] Test voice recording: `./docker-run.sh record 10`
- [ ] Test audio generation: `./docker-run.sh clone "Test"`
- [ ] Verify GPU access: `docker run --rm --gpus all nvidia/cuda:12.1.0-base nvidia-smi`

### Code Quality

- [ ] All Python scripts have proper shebangs (`#!/usr/bin/env python3`)
- [ ] Scripts are executable: `chmod +x *.sh *.py scripts/*.py`
- [ ] No hardcoded secrets or tokens in code
- [ ] `.gitignore` excludes sensitive files
- [ ] `.dockerignore` optimized for build context
- [ ] README.md updated with accurate instructions

### Documentation

- [ ] README.md has usage examples
- [ ] Docker commands are tested and accurate
- [ ] DOCKER_HUB_SETUP.md is complete
- [ ] voices/README.md has recording instructions
- [ ] All bash scripts have help text

## Docker Hub Setup

### Account Setup

- [ ] Create Docker Hub account at https://hub.docker.com
- [ ] Verify email address
- [ ] Create repository name: `voice-cloning`
- [ ] Set repository visibility (Public/Private)

### Access Token

- [ ] Generate Docker Hub access token
- [ ] Save token securely (you'll only see it once!)
- [ ] Name token: `github-actions`
- [ ] Permissions: Read, Write, Delete

### Test Local Push

- [ ] Login: `docker login`
- [ ] Tag image: `docker tag voice-cloning:latest adakrupp/voice-cloning:latest`
- [ ] Push image: `docker push adakrupp/voice-cloning:latest`
- [ ] Verify on Docker Hub: https://hub.docker.com/r/adakrupp/voice-cloning

## GitHub Setup

### Repository Creation

- [ ] Create GitHub repository: `voice-cloning`
- [ ] Add description: `Local AI voice cloning with Coqui TTS XTTS-v2`
- [ ] Choose Public/Private visibility
- [ ] Don't initialize with README (we have one)

### GitHub Secrets

Navigate to: Settings → Secrets and variables → Actions

- [ ] Add `DOCKERHUB_USERNAME` secret (your Docker Hub username)
- [ ] Add `DOCKERHUB_TOKEN` secret (Docker Hub access token)
- [ ] Verify secrets are saved correctly

### Git Configuration

- [ ] Initialize repo: `git init`
- [ ] Add remote: `git remote add origin https://github.com/adakrupp/voice-cloning.git`
- [ ] Update README with your username (replace `adakrupp`)
- [ ] Update docker-compose.yml with your image name

### Initial Commit

- [ ] Add all files: `git add .`
- [ ] Check status: `git status`
- [ ] Create commit: `git commit -m "Initial commit: Voice cloning with Docker"`
- [ ] Rename branch: `git branch -M main`
- [ ] Push to GitHub: `git push -u origin main`

## GitHub Actions Verification

### Workflow Check

- [ ] Go to GitHub repository Actions tab
- [ ] Verify "Build and Publish Docker Image" workflow is running
- [ ] Wait for build to complete (~10-15 minutes first time)
- [ ] Check for errors in workflow logs

### Build Success

- [ ] Green checkmark on workflow run
- [ ] Image pushed to Docker Hub
- [ ] Image pushed to GitHub Container Registry (ghcr.io)
- [ ] Docker Hub repository description updated

### Post-Build Verification

- [ ] Pull image: `docker pull adakrupp/voice-cloning:latest`
- [ ] Test pulled image: `docker run --rm -it adakrupp/voice-cloning python3 --version`
- [ ] Run web UI from pulled image
- [ ] Check Docker Hub for new tags

## Optional Enhancements

### Repository Settings

- [ ] Add repository description
- [ ] Add topics/tags: `voice-cloning`, `tts`, `docker`, `nvidia`, `pytorch`
- [ ] Add LICENSE file
- [ ] Enable GitHub Issues
- [ ] Enable GitHub Discussions
- [ ] Add CONTRIBUTING.md

### README Badges

Add to top of README.md:

```markdown
![Docker Build](https://github.com/adakrupp/voice-cloning/workflows/Build%20and%20Publish%20Docker%20Image/badge.svg)
![Docker Pulls](https://img.shields.io/docker/pulls/adakrupp/voice-cloning)
![Docker Image Size](https://img.shields.io/docker/image-size/adakrupp/voice-cloning/latest)
![License](https://img.shields.io/github/license/adakrupp/voice-cloning)
```

### Docker Hub Configuration

- [ ] Set repository description
- [ ] Add README from GitHub
- [ ] Enable vulnerability scanning
- [ ] Set up automated builds (optional)
- [ ] Add collaborators if needed

### Release Management

- [ ] Create first release: `git tag -a v1.0.0 -m "Initial release"`
- [ ] Push tag: `git push origin v1.0.0`
- [ ] Create GitHub Release with changelog
- [ ] Verify versioned images on Docker Hub

## Testing Checklist

### Local Docker Testing

- [ ] Build completes without errors
- [ ] Image size is reasonable (< 10GB)
- [ ] GPU detected inside container: `nvidia-smi`
- [ ] Python version correct: `python3 --version` (3.11.x)
- [ ] All dependencies installed: `pip list`
- [ ] Web UI accessible on port 7860
- [ ] Volume mounts work correctly
- [ ] Audio generation works

### Remote Image Testing

- [ ] Pull from Docker Hub works
- [ ] Pull from GitHub Packages works
- [ ] All tags available (latest, versions)
- [ ] Image runs on clean system
- [ ] Documentation matches reality

## Maintenance Tasks

### Regular Updates

- [ ] Keep Dockerfile base image updated
- [ ] Update Python dependencies: `pip list --outdated`
- [ ] Update system packages in Dockerfile
- [ ] Rebuild and push updated images
- [ ] Tag stable releases

### Monitoring

- [ ] Check Docker Hub pull statistics
- [ ] Monitor GitHub Actions usage
- [ ] Review GitHub Issues
- [ ] Check for security vulnerabilities
- [ ] Rotate Docker Hub tokens annually

## Troubleshooting Reference

### Common Issues

**Build fails in GitHub Actions:**
- Check secrets are set correctly
- Review workflow logs for errors
- Test build locally first

**Cannot pull image:**
- Verify image name matches username
- Check Docker Hub repository is public
- Try logout/login: `docker logout && docker login`

**GPU not detected:**
- Install NVIDIA Docker runtime
- Test with: `docker run --rm --gpus all nvidia/cuda:12.1.0-base nvidia-smi`
- Check docker-compose.yml has GPU configuration

**Permission denied:**
- Docker Hub token has write permissions
- GitHub secrets are set correctly
- Repository permissions allow workflows

## Post-Deployment

### Announce

- [ ] Share on social media
- [ ] Add to awesome lists
- [ ] Write blog post
- [ ] Share on relevant forums

### Documentation

- [ ] Create video tutorial
- [ ] Add example outputs
- [ ] Create troubleshooting guide
- [ ] Document common use cases

### Community

- [ ] Respond to issues
- [ ] Review pull requests
- [ ] Update documentation based on feedback
- [ ] Add contributors to README

---

## Quick Command Reference

```bash
# Local build and test
./docker-build.sh
./docker-run.sh web

# Git operations
git add .
git commit -m "Update message"
git push

# Version tagging
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0

# Docker Hub
docker login
docker push adakrupp/voice-cloning:latest

# Pull and run
docker pull adakrupp/voice-cloning:latest
docker-compose up
```

---

**Status: Ready for Deployment ✓**

Once all checklist items are complete, your voice cloning system will be fully deployed and accessible via Docker Hub and GitHub!
