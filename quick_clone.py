#!/usr/bin/env python3
"""
Quick Voice Cloning - Simple One-Command Usage
Usage: python quick_clone.py "Text to speak"
"""

import sys
import os
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.voice_cloner import VoiceCloner


# Configuration
VOICE_DIR = Path(__file__).parent / "voices" / "my_voice"
OUTPUT_DIR = Path(__file__).parent / "outputs"
DEFAULT_VOICE = VOICE_DIR / "combined.wav"


def print_usage():
    """Print usage instructions"""
    print("🎙️  Quick Voice Cloner")
    print()
    print("Usage:")
    print("  python quick_clone.py \"Your text here\"")
    print()
    print("Examples:")
    print("  python quick_clone.py \"Hello world, this is my cloned voice!\"")
    print("  python quick_clone.py \"What a beautiful day it is today!\"")
    print()
    print("First time setup:")
    print("  1. Record your voice:")
    print("     python scripts/record_voice.py 120")
    print()
    print("  2. Prepare the audio:")
    print("     python scripts/prepare_audio.py")
    print()
    print("  3. Then use this script!")
    print()


def main():
    """Main entry point"""

    # Check for text argument
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)

    # Get text from command line
    text = " ".join(sys.argv[1:])

    # Validate text
    if not text.strip():
        print("❌ Error: Text cannot be empty")
        print()
        print_usage()
        sys.exit(1)

    MAX_TEXT_LENGTH = 10000
    if len(text) > MAX_TEXT_LENGTH:
        print(f"❌ Error: Text exceeds maximum length of {MAX_TEXT_LENGTH} characters")
        sys.exit(1)

    # Check if voice file exists
    if not DEFAULT_VOICE.exists():
        print("❌ Error: Voice file not found!")
        print(f"   Expected: {DEFAULT_VOICE}")
        print()
        print("Please record your voice first:")
        print()
        print("  1. Record voice samples:")
        print("     python scripts/record_voice.py 120")
        print()
        print("  2. Prepare and combine samples:")
        print("     python scripts/prepare_audio.py")
        print()
        print("  3. Then try again:")
        print(f"     python quick_clone.py \"{text[:30]}...\"")
        print()
        sys.exit(1)

    # Create output directory
    OUTPUT_DIR.mkdir(exist_ok=True)

    # Generate unique output filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = OUTPUT_DIR / f"cloned_{timestamp}.wav"

    print()
    print("=" * 60)
    print("🎙️  Quick Voice Cloner")
    print("=" * 60)
    print()

    # Initialize voice cloner
    try:
        cloner = VoiceCloner()
    except Exception as e:
        print(f"❌ Error initializing voice cloner: {e}")
        print()
        print("Troubleshooting:")
        print("  • Make sure you've installed dependencies:")
        print("    pip install -r requirements.txt")
        print("  • For GPU support, install PyTorch with CUDA:")
        print("    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121")
        print()
        sys.exit(1)

    # Clone voice
    try:
        cloner.clone_voice(
            text=text,
            reference_audio=str(DEFAULT_VOICE),
            output_path=str(output_file)
        )
    except Exception as e:
        print(f"❌ Error generating speech: {e}")
        sys.exit(1)

    print("=" * 60)
    print("✅ Success!")
    print("=" * 60)
    print()
    print(f"📁 Output file: {output_file}")
    print(f"📏 Size: {output_file.stat().st_size / 1024:.1f} KB")
    print()

    # Try to play audio with ffplay
    try:
        import subprocess

        print("🔊 Playing audio...")
        print("   (Press 'q' or 'Esc' to stop)")
        print()

        result = subprocess.run(
            ["ffplay", "-nodisp", "-autoexit", str(output_file)],
            stderr=subprocess.DEVNULL
        )

        if result.returncode != 0:
            print("   (Audio saved but couldn't auto-play)")
            print(f"   Play manually: ffplay {output_file}")

    except FileNotFoundError:
        print("💡 Tip: Install ffplay to auto-play generated audio")
        print("   sudo pacman -S ffmpeg")
        print()
        print(f"   Or play manually: ffplay {output_file}")
        print()

    print()
    print("📝 Generate more:")
    print(f"   python quick_clone.py \"Your next sentence here\"")
    print()
    print("🚀 Try advanced features:")
    print("   python cli.py --interactive")
    print("   python web_ui.py")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
