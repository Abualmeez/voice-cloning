# Voice Cloning Docker Runner for Windows
# PowerShell script to run voice cloning Docker container

param(
    [Parameter(Position=0)]
    [string]$Command = "help",

    [Parameter(Position=1)]
    [string]$Argument = ""
)

$IMAGE_NAME = "adakrupp/voice-cloning:latest"
$CONTAINER_NAME = "voice-cloning-app"

# Colors for output (if terminal supports it)
function Write-Success { Write-Host $args -ForegroundColor Green }
function Write-Warning { Write-Host $args -ForegroundColor Yellow }
function Write-Error { Write-Host $args -ForegroundColor Red }

# Common Docker options
$DOCKER_OPTS = @(
    "--rm"
    "-it"
    "--name", $CONTAINER_NAME
    "-v", "${PWD}/voices:/app/voices"
    "-v", "${PWD}/outputs:/app/outputs"
    "-v", "${PWD}/models:/app/models"
)

# Check if running in WSL2 (for GPU support)
$inWSL = $env:WSL_DISTRO_NAME -ne $null

switch ($Command.ToLower()) {
    "web" {
        Write-Success "Starting web UI..."
        Write-Host "Access at: http://localhost:7860"
        Write-Host ""
        if ($inWSL) {
            Write-Success "WSL2 detected - GPU support enabled"
            $DOCKER_OPTS += "--gpus", "all"
        } else {
            Write-Warning "⚠️  Running on CPU (slower). For GPU support, use WSL2."
            Write-Warning "   Generate time: 30-60s per sentence (vs 5-10s with GPU)"
        }
        Write-Host ""

        docker run @DOCKER_OPTS `
            -p 7860:7860 `
            $IMAGE_NAME `
            python3 web_ui.py --host 0.0.0.0 --port 7860
    }

    "cli" {
        Write-Success "Starting interactive CLI..."
        if ($inWSL) {
            $DOCKER_OPTS += "--gpus", "all"
        }

        docker run @DOCKER_OPTS `
            $IMAGE_NAME `
            python3 cli.py --interactive
    }

    "record" {
        $duration = if ($Argument) { $Argument } else { "120" }
        Write-Success "Starting voice recording for $duration seconds..."
        Write-Warning "Note: Microphone access in Docker may not work on Windows"
        Write-Warning "Consider recording directly with: python scripts/record_voice.py $duration"

        docker run @DOCKER_OPTS `
            $IMAGE_NAME `
            python3 scripts/record_voice.py $duration
    }

    "clone" {
        if (-not $Argument) {
            Write-Error "Error: Please provide text to synthesize"
            Write-Host 'Usage: .\docker-run.ps1 clone "Your text here"'
            exit 1
        }

        Write-Success "Generating speech..."
        if ($inWSL) {
            $DOCKER_OPTS += "--gpus", "all"
        }

        docker run @DOCKER_OPTS `
            $IMAGE_NAME `
            python3 quick_clone.py $Argument
    }

    "bash" {
        Write-Success "Starting bash shell in container..."
        if ($inWSL) {
            $DOCKER_OPTS += "--gpus", "all"
        }

        docker run @DOCKER_OPTS `
            $IMAGE_NAME `
            /bin/bash
    }

    "pull" {
        Write-Success "Pulling latest Docker image..."
        docker pull $IMAGE_NAME
    }

    "help" {
        Write-Host ""
        Write-Host "Voice Cloning Docker Runner (Windows)" -ForegroundColor Cyan
        Write-Host "=====================================" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "Usage: .\docker-run.ps1 <command> [arguments]"
        Write-Host ""
        Write-Host "Commands:" -ForegroundColor Yellow
        Write-Host "  web              Start web UI (http://localhost:7860)"
        Write-Host "  cli              Start interactive command-line interface"
        Write-Host "  record [seconds] Record voice sample (default: 120 seconds)"
        Write-Host '  clone "text"     Generate speech from text'
        Write-Host "  bash             Open bash shell in container"
        Write-Host "  pull             Pull latest Docker image"
        Write-Host "  help             Show this help message"
        Write-Host ""
        Write-Host "Examples:" -ForegroundColor Yellow
        Write-Host '  .\docker-run.ps1 web'
        Write-Host '  .\docker-run.ps1 clone "Hello, this is my cloned voice!"'
        Write-Host '  .\docker-run.ps1 record 180'
        Write-Host ""
        Write-Host "GPU Support:" -ForegroundColor Yellow
        if ($inWSL) {
            Write-Success "  ✓ Running in WSL2 - GPU acceleration enabled"
        } else {
            Write-Warning "  ⚠ Running in Windows - CPU only (slower)"
            Write-Host "  For GPU support, run this script from WSL2:"
            Write-Host "    wsl"
            Write-Host "    cd ~/voice-cloning"
            Write-Host "    ./docker-run.sh web"
        }
        Write-Host ""
    }

    default {
        Write-Error "Unknown command: $Command"
        Write-Host ""
        Write-Host "Run '.\docker-run.ps1 help' for usage information"
        exit 1
    }
}
