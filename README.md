# 🎙️ Voice Cloning Studio

Local AI voice cloning system that lets you type text and hear it spoken in your own voice. Runs 100% offline using Coqui TTS XTTS-v2.

## Features

- **Zero-shot voice cloning** - No training required, just 1-5 minutes of your voice
- **Fast generation** - 5-10 seconds per sentence on GPU
- **High quality** - Commercial-grade voice synthesis
- **Multi-language** - 17+ languages supported
- **Multiple interfaces** - Simple CLI, advanced CLI, and web UI
- **100% local** - No internet required after setup
- **GPU accelerated** - Optimized for NVIDIA GPUs

## Prerequisites

Before you begin, ensure you have the following installed:

### Docker Installation (Recommended)

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install docker.io docker-compose
sudo systemctl start docker
sudo systemctl enable docker
```

**Arch Linux:**
```bash
sudo pacman -S docker docker-compose
sudo systemctl start docker
sudo systemctl enable docker
```

**Add your user to docker group (to avoid sudo):**
```bash
sudo usermod -aG docker $USER
newgrp docker  # Or logout/login
```

### NVIDIA Docker Runtime (for GPU support)

**Ubuntu/Debian:**
```bash
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | \
  sudo tee /etc/apt/sources.list.d/nvidia-docker.list
sudo apt-get update && sudo apt-get install -y nvidia-docker2
sudo systemctl restart docker
```

**Arch Linux:**
```bash
sudo pacman -S nvidia-container-toolkit
sudo systemctl restart docker
```

**Test GPU access:**
```bash
docker run --rm --gpus all nvidia/cuda:12.1.0-base-ubuntu22.04 nvidia-smi
```

### Python 3.11 (for manual installation)

**Ubuntu/Debian:**
```bash
sudo apt install python3.11 python3.11-venv python3.11-dev
```

**Arch Linux:**
```bash
sudo pacman -S python
```

## Quick Start

### 🐳 Docker (Recommended)

The easiest way to get started. No Python version conflicts, all dependencies included.

**Prerequisites:**
- Docker and Docker Compose
- NVIDIA Docker runtime (for GPU support)

**Run with Docker Compose:**
```bash
# Start web UI
docker-compose up

# Access at http://localhost:7860
```

**Or use helper scripts:**
```bash
# Build image
./docker-build.sh

# Run web UI
./docker-run.sh web

# Run interactive CLI
./docker-run.sh cli

# Record voice
./docker-run.sh record 120

# Generate speech
./docker-run.sh clone "Hello world!"
```

**Pull from Docker Hub:**
```bash
# Pull pre-built image (once published)
docker pull adakrupp/voice-cloning:latest

# Run web UI
docker run --rm -it --gpus all \
  -p 7860:7860 \
  -v $(pwd)/voices:/app/voices \
  -v $(pwd)/outputs:/app/outputs \
  adakrupp/voice-cloning:latest \
  python3 web_ui.py --host 0.0.0.0
```

### 📦 Manual Installation (Alternative)

**Note:** Requires Python 3.9-3.11 (Python 3.13+ not supported by Coqui TTS)

```bash
cd voice-cloning

# Install Python 3.11 if needed
sudo pacman -S python311  # Arch Linux
# or
sudo apt install python3.11  # Ubuntu/Debian

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip wheel setuptools

# Install PyTorch with CUDA support
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# Install voice cloning packages
pip install TTS librosa soundfile pydub sounddevice gradio

# Install system dependency (for recording)
sudo pacman -S portaudio
```

### 2. Record Your Voice

```bash
# Record for 2 minutes (recommended)
python scripts/record_voice.py 120

# Or record multiple samples
python scripts/record_voice.py 60
python scripts/record_voice.py 60
```

**Recording tips:**
- Find a quiet environment (no background noise)
- Speak naturally and clearly
- Vary your tone and emotion
- Read the sample script in `voices/README.md`

### 3. Prepare Audio

```bash
# Clean and combine voice samples
python scripts/prepare_audio.py
```

This creates `voices/my_voice/combined.wav` - your voice profile.

### 4. Verify Installation

After setup, verify everything is working:

**Check GPU access (if applicable):**
```bash
python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}')"
# Should print: CUDA available: True
```

**Verify TTS is installed:**
```bash
python -c "from TTS.api import TTS; print('TTS installed successfully')"
```

**Test voice generation:**
```bash
# This will download the model on first run (~2GB, 5-10 minutes)
python quick_clone.py "This is a test"
# Should create audio file in outputs/
```

### 5. Start Cloning!

```bash
# Simple usage
python quick_clone.py "Hello world, this is my cloned voice!"

# Interactive mode
python cli.py --interactive

# Web interface
python web_ui.py
```

## Usage

### Quick Clone (Simplest)

One command to generate speech:

```bash
python quick_clone.py "Your text here"
```

Auto-generates timestamped file in `outputs/` and plays it.

### Advanced CLI

Full-featured command-line interface:

```bash
# Interactive mode (recommended)
python cli.py --interactive

# Generate specific file
python cli.py --text "Hello" --output greeting.wav

# Use different language
python cli.py --text "Bonjour le monde" --language fr

# List available voices
python cli.py --list-voices
```

**Interactive mode** lets you type continuously and hear each response:
```
python cli.py --interactive
[1] (en) > Hello, how are you today?
🎤 Generating: 'Hello, how are you today?'
✅ Audio saved to: outputs/interactive_20260107_123456_001.wav

[2] (en) > lang es
✓ Language changed to: es

[3] (es) > Hola, ¿cómo estás?
🎤 Generating: 'Hola, ¿cómo estás?'
✅ Audio saved to: outputs/interactive_20260107_123457_002.wav
```

### Web UI

Browser-based interface with visual controls:

```bash
python web_ui.py
```

Opens http://localhost:7860 in your browser with:
- Text input box
- Voice selection dropdown
- Language selector
- Audio player
- Example prompts

## Supported Languages

English (en), Spanish (es), French (fr), German (de), Italian (it), Portuguese (pt), Polish (pl), Turkish (tr), Russian (ru), Dutch (nl), Czech (cs), Arabic (ar), Chinese (zh-cn), Japanese (ja), Hungarian (hu), Korean (ko)

## Project Structure

```
voice-cloning/
├── src/
│   ├── __init__.py
│   └── voice_cloner.py          # Core TTS wrapper
├── scripts/
│   ├── record_voice.py          # Record microphone
│   └── prepare_audio.py         # Clean & combine audio
├── voices/
│   └── my_voice/                # Your voice samples
│       ├── sample_*.wav         # Recordings
│       └── combined.wav         # Processed voice
├── outputs/                     # Generated audio files
├── quick_clone.py               # Simple CLI
├── cli.py                       # Advanced CLI
├── web_ui.py                    # Web interface
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## System Requirements

**Minimum:**
- Linux (tested on Arch/Manjaro)
- Python 3.9+
- 8GB RAM
- 4GB free disk space

**Recommended:**
- NVIDIA GPU with 8GB+ VRAM (RTX 3060 or better)
- 16GB+ RAM
- SSD storage

**Tested on:**
- Linux 6.12.63-1-lts
- Python 3.13
- NVIDIA RTX 4070 Ti SUPER (16GB VRAM)

## How It Works

### Technology

Uses **Coqui TTS XTTS-v2** - a state-of-the-art voice cloning model:
- Zero-shot cloning (no training required)
- Reference audio analysis for voice characteristics
- Cross-lingual voice cloning
- Real-time synthesis on GPU

### Process

1. **Reference audio** - Load your voice sample (1-5 minutes)
2. **Text input** - Type what you want to say
3. **Voice analysis** - Model analyzes voice characteristics
4. **Speech synthesis** - Generate audio matching your voice
5. **Output** - Save as WAV file

### Performance

**First run:** 2-5 minutes (downloads ~2GB model)

**Subsequent runs:**
- GPU (RTX 4070 Ti): ~5-10 seconds per sentence
- CPU: ~30-60 seconds per sentence

**VRAM usage:** ~4-6GB

## Advanced Usage

### Multiple Voice Profiles

Create different voice profiles for different moods/styles:

```bash
# Record excited voice
mkdir voices/my_excited_voice
python scripts/record_voice.py 120  # Record excitedly!
# Save to voices/my_excited_voice/
python scripts/prepare_audio.py --voice-dir voices/my_excited_voice

# Use it
python cli.py --voice my_excited_voice --text "Wow, this is amazing!"
```

### Batch Processing

Generate multiple files at once:

```bash
# Create a text file with your sentences
cat > sentences.txt <<EOF
Hello, this is sentence one.
This is sentence two.
And here's sentence three.
EOF

# Generate all
while IFS= read -r line; do
    python quick_clone.py "$line"
done < sentences.txt
```

### Custom Output Location

```bash
python cli.py --text "Test" --output ~/Desktop/my_voice.wav
```

## Docker Deployment

### Building the Image

```bash
# Build locally
./docker-build.sh

# Or with docker command
docker build -t voice-cloning:latest .

# Build with specific tag
./docker-build.sh v1.0.0
```

### Running with Docker Compose

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Run CLI instead of web UI
docker-compose --profile cli up voice-cloning-cli
```

### Docker Hub Publishing

**Setup (One-time):**

1. Create Docker Hub account at https://hub.docker.com
2. Add GitHub secrets:
   - `DOCKERHUB_USERNAME` - Your Docker Hub username
   - `DOCKERHUB_TOKEN` - Docker Hub access token

**Automated Publishing:**

GitHub Actions automatically builds and pushes to Docker Hub on:
- Push to `main` branch → `latest` tag
- Push tag `v*.*.*` → version tags
- Pull requests → test build only

**Manual Publishing:**

```bash
# Login to Docker Hub
docker login

# Tag image
docker tag voice-cloning:latest adakrupp/voice-cloning:latest
docker tag voice-cloning:latest adakrupp/voice-cloning:v1.0.0

# Push to Docker Hub
docker push adakrupp/voice-cloning:latest
docker push adakrupp/voice-cloning:v1.0.0
```

### GitHub Container Registry

Images are also published to `ghcr.io`:

```bash
# Pull from GitHub Container Registry
docker pull ghcr.io/adakrupp/voice-cloning:latest

# Use in docker-compose.yml
image: ghcr.io/adakrupp/voice-cloning:latest
```

### Docker Environment Variables

```bash
# GPU configuration
NVIDIA_VISIBLE_DEVICES=all
NVIDIA_DRIVER_CAPABILITIES=compute,utility

# Custom model cache location
MODEL_CACHE_DIR=/custom/path

# Run in CPU mode (if no GPU)
docker run --rm -it \
  -p 7860:7860 \
  voice-cloning:latest
```

### Volume Mounts

Persist data between container runs:

```yaml
volumes:
  - ./voices:/app/voices        # Voice samples
  - ./outputs:/app/outputs      # Generated audio
  - ./models:/app/models        # Model cache
```

### GPU Support

**Install NVIDIA Docker Runtime:**

```bash
# Ubuntu/Debian
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | \
  sudo tee /etc/apt/sources.list.d/nvidia-docker.list
sudo apt-get update && sudo apt-get install -y nvidia-docker2
sudo systemctl restart docker

# Test GPU access
docker run --rm --gpus all nvidia/cuda:12.1.0-base-ubuntu22.04 nvidia-smi
```

## Troubleshooting

### Setup and Installation Issues

**Docker permission denied:**
```bash
# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker
```

**TTS Installation fails:**
```bash
# Install build dependencies
sudo apt install build-essential python3-dev  # Ubuntu/Debian
sudo pacman -S base-devel                     # Arch Linux

# Try with pre-built wheels
pip install --prefer-binary TTS
```

**PyTorch CUDA version mismatch:**
```bash
# Check your CUDA version
nvidia-smi

# Install matching PyTorch (example for CUDA 11.8)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

**Docker GPU not detected:**
```bash
# Verify NVIDIA Docker runtime
docker run --rm --gpus all nvidia/cuda:12.1.0-base-ubuntu22.04 nvidia-smi

# If fails, reinstall nvidia-docker2
sudo apt install nvidia-docker2
sudo systemctl restart docker
```

**Port 7860 already in use:**
```bash
# Use different port
docker run ... -p 7861:7860 ...
# or
python web_ui.py --port 7861
```

### No audio generated

**Problem:** Generation completes but no sound

**Solution:**
- Check `outputs/` directory for WAV files
- Install ffplay: `sudo pacman -S ffmpeg`
- Try playing manually: `ffplay outputs/cloned_*.wav`

### Poor quality output

**Problem:** Voice doesn't sound like you

**Solutions:**
- Record more samples (aim for 2-5 minutes total)
- Record in quieter environment
- Speak more clearly and naturally
- Use better microphone
- Re-run `python scripts/prepare_audio.py`

### CUDA out of memory

**Problem:** GPU memory error during generation

**Solutions:**
- Close other GPU applications
- Use CPU instead (slower): Set `device="cpu"` in `src/voice_cloner.py`
- Reduce batch size

### Microphone not detected

**Problem:** Recording script can't find microphone

**Solutions:**
```bash
# List audio devices
python scripts/record_voice.py --list-devices

# Use specific device
python scripts/record_voice.py --device 1

# Check system audio
arecord -l
```

### Model download fails

**Problem:** First run can't download model

**Solutions:**
- Check internet connection
- Try again (downloads can be interrupted)
- Manually download from Coqui TTS
- Check firewall/proxy settings

### Import errors

**Problem:** `ModuleNotFoundError` when running

**Solutions:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt

# Check PyTorch CUDA
python -c "import torch; print(torch.cuda.is_available())"
```

## Tips for Best Results

### Recording Quality

- **Quiet environment** - No fans, AC, traffic, or background noise
- **Consistent distance** - Stay 6-12 inches from mic
- **Good microphone** - Use USB mic or quality headset
- **No echo** - Avoid large empty rooms
- **Pop filter** - Reduce plosives (P, B sounds)

### Speaking Style

- **Natural pace** - Don't rush or speak too slowly
- **Clear articulation** - Pronounce words clearly
- **Varied emotion** - Include questions, excitement, calm statements
- **Natural pauses** - Brief pauses are fine
- **Varied content** - Read different types of sentences

### Content Variety

Record a mix of:
- Simple statements
- Questions
- Exclamations
- Long and short sentences
- Different emotions

See `voices/README.md` for sample recording script.

## FAQ

**Q: How much of my voice do I need to record?**
A: Minimum 30 seconds, recommended 1-5 minutes. More varied content is better than just length.

**Q: Can I use this for other people's voices?**
A: Only with explicit permission. Voice cloning should be used ethically and legally.

**Q: Does it work without a GPU?**
A: Yes, but it's slower (30-60 seconds vs 5-10 seconds per sentence).

**Q: Can I clone voices in different languages?**
A: Yes! Record in any language, then generate speech in 17+ languages.

**Q: How big are the generated files?**
A: ~100-500KB per sentence (WAV format, 22050Hz mono).

**Q: Does it need internet?**
A: Only for initial model download (~2GB). After that, 100% offline.

**Q: Can I use generated audio commercially?**
A: Check Coqui TTS license. Generally OK for personal use.

**Q: Why is first run slow?**
A: Downloads the model (~2GB). Subsequent runs are fast.

## Security & Privacy

### For Production Use

If deploying this publicly:

1. **Enable authentication:**
   ```bash
   python web_ui.py --auth username password
   ```

2. **Use HTTPS with reverse proxy:**
   ```bash
   # Use nginx or traefik with SSL certificates
   # Don't expose web UI directly to internet
   ```

3. **Bind to localhost only:**
   ```bash
   python web_ui.py --host 127.0.0.1
   ```

4. **Keep dependencies updated:**
   ```bash
   pip install --upgrade TTS torch gradio
   ```

### Voice Cloning Ethics

**Important Considerations:**
- Only clone voices with explicit permission
- Don't impersonate or deceive others
- Respect privacy and consent
- Check local laws regarding voice synthesis
- Use for personal/educational purposes only

### Data Privacy

- Voice samples stay on your machine (100% local processing)
- No data sent to external services (except model download)
- Delete voice samples when no longer needed
- Don't commit voice files to git repositories

## Credits

- **Coqui TTS** - Voice cloning model (XTTS-v2)
- **PyTorch** - Deep learning framework
- **Gradio** - Web interface
- **librosa** - Audio processing

## License

This project is for personal/educational use. Check individual component licenses:
- Coqui TTS: Mozilla Public License 2.0
- PyTorch: BSD License
- Other dependencies: See their respective licenses

## Disclaimer

Voice cloning technology should be used responsibly and ethically. Only clone voices you have permission to use. Misuse of voice cloning technology may violate laws regarding fraud, impersonation, or privacy.

## Support

For issues or questions:
1. Check troubleshooting section above
2. Review `voices/README.md` for recording tips
3. Ensure all dependencies are installed
4. Check system requirements

---

**Enjoy cloning your voice! 🎤**

## Docker Hub

Pre-built Docker images are available:

```bash
docker pull adakrupp/voice-cloning:latest
```

[![Docker Hub](https://img.shields.io/docker/pulls/adakrupp/voice-cloning)](https://hub.docker.com/r/adakrupp/voice-cloning)
