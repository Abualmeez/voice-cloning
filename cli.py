#!/usr/bin/env python3
"""
Advanced Voice Cloning CLI
Full-featured command-line interface with interactive mode
"""

import argparse
from pathlib import Path
import sys
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.voice_cloner import VoiceCloner, validate_path


def find_voice_file(voice_name):
    """
    Find voice file for given voice name

    Args:
        voice_name: Name of voice directory or path to wav file

    Returns:
        Path to voice file or None
    """
    # If it's a direct path to a file, validate it's in voices directory
    if Path(voice_name).exists() and Path(voice_name).suffix == ".wav":
        try:
            validated_path = validate_path(voice_name, "voices")
            return validated_path
        except ValueError:
            # Path is outside voices directory, skip it
            pass

    # Look in voices directory
    voices_dir = Path("voices")

    # Try combined.wav in voice directory
    combined_path = voices_dir / voice_name / "combined.wav"
    if combined_path.exists():
        return combined_path

    # Try to find any wav file in voice directory
    voice_dir = voices_dir / voice_name
    if voice_dir.exists() and voice_dir.is_dir():
        wav_files = list(voice_dir.glob("*.wav"))
        if wav_files:
            return wav_files[0]

    return None


def list_voices():
    """List all available voice profiles"""
    voices_dir = Path("voices")

    if not voices_dir.exists():
        print("No voices directory found.")
        return

    print("\n📂 Available Voice Profiles:")
    print("=" * 50)

    found_any = False

    for voice_dir in sorted(voices_dir.iterdir()):
        if voice_dir.is_dir() and not voice_dir.name.startswith("."):
            wav_files = list(voice_dir.glob("*.wav"))

            if wav_files:
                found_any = True
                print(f"\n  🎤 {voice_dir.name}")

                # Show combined.wav if it exists
                combined = voice_dir / "combined.wav"
                if combined.exists():
                    size_kb = combined.stat().st_size / 1024
                    print(f"     ✓ combined.wav ({size_kb:.1f} KB) - Ready to use!")

                # Show sample files
                samples = [f for f in wav_files if f.name.startswith("sample_")]
                if samples:
                    print(f"     • {len(samples)} sample file(s)")

    if not found_any:
        print("\n  No voice profiles found.")
        print("\n  Create one by running:")
        print("    python scripts/record_voice.py")
        print("    python scripts/prepare_audio.py")

    print()


def interactive_mode(cloner, voice_file):
    """
    Interactive text-to-speech session

    Args:
        cloner: VoiceCloner instance
        voice_file: Path to voice reference audio
    """
    print("\n" + "=" * 60)
    print("🎙️  Interactive Voice Cloning Mode")
    print("=" * 60)
    print()
    print("Type your text and press Enter to generate speech.")
    print("Commands:")
    print("  • Type text to generate speech")
    print("  • 'quit' or 'exit' - Exit interactive mode")
    print("  • 'lang <code>' - Change language (e.g., 'lang es')")
    print("  • 'help' - Show this help")
    print()

    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)

    counter = 1
    current_language = "en"

    while True:
        try:
            # Prompt
            user_input = input(f"\n[{counter}] ({current_language}) > ").strip()

            # Handle empty input
            if not user_input:
                continue

            # Handle commands
            if user_input.lower() in ["quit", "exit", "q"]:
                print("\n👋 Goodbye!")
                break

            if user_input.lower() == "help":
                print("\nCommands:")
                print("  • Type text to generate speech")
                print("  • 'quit' or 'exit' - Exit")
                print("  • 'lang <code>' - Change language")
                print("  • 'help' - Show this help")
                print("\nSupported languages:")
                print("  en, es, fr, de, it, pt, pl, tr, ru, nl, cs, ar, zh-cn, ja, hu, ko")
                continue

            if user_input.lower().startswith("lang "):
                new_lang = user_input.split()[1].lower()
                supported = cloner.get_supported_languages()

                if new_lang in supported:
                    current_language = new_lang
                    print(f"✓ Language changed to: {current_language}")
                else:
                    print(f"✗ Unsupported language: {new_lang}")
                    print(f"  Supported: {', '.join(supported)}")
                continue

            # Generate speech
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = output_dir / f"interactive_{timestamp}_{counter:03d}.wav"

            try:
                cloner.clone_voice(
                    text=user_input,
                    reference_audio=str(voice_file),
                    output_path=str(output_file),
                    language=current_language
                )

                print(f"💾 Saved: {output_file.name}")

                # Try to play audio
                try:
                    import subprocess
                    subprocess.run(
                        ["ffplay", "-nodisp", "-autoexit", str(output_file)],
                        stderr=subprocess.DEVNULL,
                        stdout=subprocess.DEVNULL
                    )
                except:
                    pass

                counter += 1

            except Exception as e:
                print(f"❌ Error: {e}")

        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break

        except EOFError:
            print("\n\n👋 Goodbye!")
            break


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Advanced Voice Cloning CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode (recommended)
  python cli.py --interactive

  # Generate single file
  python cli.py --text "Hello world!" --output greeting.wav

  # Use specific voice profile
  python cli.py --voice my_voice --text "Testing" --output test.wav

  # Generate in different language
  python cli.py --text "Bonjour le monde" --language fr

  # List available voices
  python cli.py --list-voices

Supported Languages:
  en (English), es (Spanish), fr (French), de (German), it (Italian),
  pt (Portuguese), pl (Polish), tr (Turkish), ru (Russian), nl (Dutch),
  cs (Czech), ar (Arabic), zh-cn (Chinese), ja (Japanese), hu (Hungarian),
  ko (Korean)
        """
    )

    parser.add_argument(
        "--text", "-t",
        help="Text to synthesize"
    )

    parser.add_argument(
        "--voice", "-v",
        default="my_voice",
        help="Voice profile name or path to wav file (default: my_voice)"
    )

    parser.add_argument(
        "--output", "-o",
        help="Output file path (default: auto-generated in outputs/)"
    )

    parser.add_argument(
        "--language", "-l",
        default="en",
        help="Language code (default: en)"
    )

    parser.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="Interactive mode - continuous text-to-speech session"
    )

    parser.add_argument(
        "--list-voices",
        action="store_true",
        help="List available voice profiles and exit"
    )

    args = parser.parse_args()

    # List voices
    if args.list_voices:
        list_voices()
        return

    # Find voice file
    voice_file = find_voice_file(args.voice)

    if not voice_file:
        print(f"❌ Error: Voice profile '{args.voice}' not found")
        print()
        list_voices()
        print("Create a new voice profile:")
        print("  1. python scripts/record_voice.py")
        print("  2. python scripts/prepare_audio.py")
        sys.exit(1)

    print(f"\n🎤 Using voice: {voice_file}")

    # Initialize voice cloner
    print()
    try:
        cloner = VoiceCloner()
    except Exception as e:
        print(f"❌ Error initializing voice cloner: {e}")
        print()
        print("Make sure you've installed dependencies:")
        print("  pip install -r requirements.txt")
        sys.exit(1)

    # Interactive mode
    if args.interactive:
        interactive_mode(cloner, voice_file)
        return

    # Single generation mode
    if not args.text:
        print("❌ Error: --text required (or use --interactive)")
        print()
        parser.print_help()
        sys.exit(1)

    # Validate text length
    MAX_TEXT_LENGTH = 10000
    if len(args.text) > MAX_TEXT_LENGTH:
        print(f"❌ Error: Text exceeds maximum length of {MAX_TEXT_LENGTH} characters")
        sys.exit(1)

    # Generate output path
    if args.output:
        # Validate output path is within outputs directory
        try:
            output_path = validate_path(args.output, "outputs")
        except ValueError:
            print(f"❌ Error: Output path must be within outputs/ directory")
            sys.exit(1)
    else:
        output_dir = Path("outputs")
        output_dir.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = output_dir / f"output_{timestamp}.wav"

    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Generate speech
    print()
    try:
        cloner.clone_voice(
            text=args.text,
            reference_audio=str(voice_file),
            output_path=str(output_path),
            language=args.language
        )

        print("=" * 60)
        print("✅ Success!")
        print("=" * 60)
        print(f"📁 Output: {output_path}")
        print(f"📏 Size: {output_path.stat().st_size / 1024:.1f} KB")
        print()

    except Exception as e:
        print(f"❌ Error generating speech: {e}")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Cancelled by user")
        sys.exit(1)
