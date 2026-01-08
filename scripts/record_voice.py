#!/usr/bin/env python3
"""
Voice Recording Script
Record voice samples from microphone for voice cloning
"""

import sounddevice as sd
import soundfile as sf
import numpy as np
from datetime import datetime
from pathlib import Path
import sys
import time


# Recording configuration
SAMPLE_RATE = 22050  # Hz (optimal for XTTS-v2)
CHANNELS = 1  # Mono
DEFAULT_DURATION = 120  # 2 minutes


def list_audio_devices():
    """List available audio input devices"""
    print("\n=== Available Audio Devices ===")
    print(sd.query_devices())
    print()


def record_audio(duration_seconds, output_path=None, device=None):
    """
    Record audio from microphone

    Args:
        duration_seconds: How long to record (in seconds)
        output_path: Where to save the recording
        device: Audio input device index (None for default)

    Returns:
        Path to saved audio file
    """
    print("\n🎙️  Voice Recording Tool")
    print("=" * 50)
    print(f"⏱️  Duration: {duration_seconds} seconds ({duration_seconds/60:.1f} minutes)")
    print(f"🎚️  Sample Rate: {SAMPLE_RATE} Hz")
    print(f"📻 Channels: Mono")
    print()

    # Generate output path if not provided
    if output_path is None:
        # Create voices/my_voice directory if it doesn't exist
        voices_dir = Path(__file__).parent.parent / "voices" / "my_voice"
        voices_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = voices_dir / f"sample_{timestamp}.wav"

    output_path = Path(output_path)

    # Recording tips
    print("📝 Recording Tips:")
    print("   • Find a quiet environment (no background noise)")
    print("   • Speak naturally and clearly")
    print("   • Vary your tone and emotion")
    print("   • Read varied sentences (see voices/README.md)")
    print("   • Maintain consistent distance from microphone")
    print()

    # Countdown
    print("🔴 Recording starts in...")
    for i in range(3, 0, -1):
        print(f"   {i}...")
        time.sleep(1)

    print()
    print("🔴 RECORDING NOW! Speak clearly...")
    print(f"   (Recording for {duration_seconds} seconds)")
    print()

    # Record audio
    try:
        audio = sd.rec(
            int(duration_seconds * SAMPLE_RATE),
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            dtype=np.float32,
            device=device
        )
        sd.wait()  # Wait until recording is finished

        print("✅ Recording complete!")
        print()

        # Check if audio is not silent
        max_amplitude = np.max(np.abs(audio))
        if max_amplitude < 0.001:
            print("⚠️  WARNING: Recording appears to be silent!")
            print("   Check your microphone settings and try again.")
            print()
            return None

        # Save audio
        sf.write(str(output_path), audio, SAMPLE_RATE)

        print(f"💾 Saved to: {output_path}")
        print(f"📊 Duration: {len(audio)/SAMPLE_RATE:.1f} seconds")
        print(f"📏 Size: {output_path.stat().st_size / 1024:.1f} KB")
        print(f"🔊 Max amplitude: {max_amplitude:.3f}")
        print()

        return output_path

    except Exception as e:
        print(f"❌ Error recording audio: {e}")
        print()
        print("Troubleshooting:")
        print("  • Check if microphone is connected")
        print("  • Try running: python -c \"import sounddevice as sd; print(sd.query_devices())\"")
        print("  • Install portaudio: sudo pacman -S portaudio")
        print()
        return None


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Record voice samples for voice cloning",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Record for 2 minutes (default)
  python scripts/record_voice.py

  # Record for 1 minute
  python scripts/record_voice.py 60

  # Record for 5 minutes
  python scripts/record_voice.py 300

  # List available audio devices
  python scripts/record_voice.py --list-devices

  # Use specific audio device
  python scripts/record_voice.py --device 1

After recording, prepare audio with:
  python scripts/prepare_audio.py
        """
    )

    parser.add_argument(
        "duration",
        nargs="?",
        type=int,
        default=DEFAULT_DURATION,
        help=f"Recording duration in seconds (default: {DEFAULT_DURATION})"
    )

    parser.add_argument(
        "--output", "-o",
        help="Output file path (default: auto-generated in voices/my_voice/)"
    )

    parser.add_argument(
        "--device", "-d",
        type=int,
        help="Audio input device index"
    )

    parser.add_argument(
        "--list-devices", "-l",
        action="store_true",
        help="List available audio devices and exit"
    )

    args = parser.parse_args()

    # List devices and exit
    if args.list_devices:
        list_audio_devices()
        return

    # Validate duration
    if args.duration < 5:
        print("❌ Error: Duration must be at least 5 seconds")
        return

    if args.duration > 600:
        print("⚠️  Warning: Recording for more than 10 minutes")
        response = input("Continue? [y/N]: ")
        if response.lower() != "y":
            print("Cancelled.")
            return

    # Record audio
    output_path = record_audio(args.duration, args.output, args.device)

    if output_path:
        print("✅ Success!")
        print()
        print("Next steps:")
        print("  1. Record more samples (optional, for variety)")
        print("  2. Prepare audio: python scripts/prepare_audio.py")
        print("  3. Test voice clone: python quick_clone.py \"Hello world!\"")
        print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Recording cancelled by user")
        sys.exit(1)
