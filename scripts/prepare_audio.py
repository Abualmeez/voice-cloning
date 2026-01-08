#!/usr/bin/env python3
"""
Audio Preparation Script
Clean, normalize, and combine voice samples for voice cloning
"""

from pydub import AudioSegment
from pydub.silence import detect_nonsilent
import os
import glob
from pathlib import Path
import sys


def prepare_audio(input_path, output_path=None):
    """
    Clean and prepare audio for voice cloning

    Args:
        input_path: Path to input audio file
        output_path: Path to save processed audio (optional)

    Returns:
        Path to processed audio file
    """
    print(f"📁 Processing: {Path(input_path).name}")

    # Load audio
    try:
        audio = AudioSegment.from_file(input_path)
    except Exception as e:
        print(f"❌ Error loading audio: {e}")
        return None

    original_duration = len(audio) / 1000

    # Convert to mono
    if audio.channels > 1:
        print("   • Converting to mono...")
        audio = audio.set_channels(1)

    # Set sample rate to 22050 Hz (optimal for XTTS-v2)
    if audio.frame_rate != 22050:
        print(f"   • Converting sample rate: {audio.frame_rate} Hz → 22050 Hz")
        audio = audio.set_frame_rate(22050)

    # Normalize volume
    print("   • Normalizing volume...")
    audio = audio.normalize()

    # Remove leading/trailing silence
    print("   • Removing silence...")
    nonsilent_ranges = detect_nonsilent(
        audio,
        min_silence_len=500,  # 500ms minimum silence
        silence_thresh=-40    # -40dB threshold
    )

    if nonsilent_ranges:
        start, end = nonsilent_ranges[0][0], nonsilent_ranges[-1][1]
        audio = audio[start:end]
    else:
        print("   ⚠️  Warning: No non-silent audio detected")

    # Generate output path if not provided
    if output_path is None:
        output_path = str(Path(input_path).with_suffix(".processed.wav"))

    # Export as WAV
    audio.export(output_path, format="wav")

    processed_duration = len(audio) / 1000

    print(f"✅ Saved to: {Path(output_path).name}")
    print(f"   Duration: {original_duration:.1f}s → {processed_duration:.1f}s")
    print(f"   Size: {Path(output_path).stat().st_size / 1024:.1f} KB")
    print()

    return output_path


def combine_samples(voice_dir, output_name="combined.wav"):
    """
    Combine multiple voice samples into one file

    Args:
        voice_dir: Directory containing voice samples
        output_name: Output filename (default: combined.wav)

    Returns:
        Path to combined audio file
    """
    voice_dir = Path(voice_dir)

    # Find all sample files
    samples = sorted(glob.glob(str(voice_dir / "sample_*.wav")))

    if not samples:
        print(f"❌ No voice samples found in {voice_dir}")
        print("   Expected files: sample_*.wav")
        return None

    print(f"\n🔗 Combining {len(samples)} samples...")
    print()

    combined = AudioSegment.empty()

    for i, sample in enumerate(samples, 1):
        print(f"   [{i}/{len(samples)}] {Path(sample).name}")
        try:
            audio = AudioSegment.from_wav(sample)
            combined += audio
            # Add 500ms pause between samples
            combined += AudioSegment.silent(duration=500)
        except Exception as e:
            print(f"      ⚠️  Warning: Failed to load {sample}: {e}")

    # Remove trailing silence
    combined = combined[:-500]  # Remove last pause

    # Save combined audio
    output_path = voice_dir / output_name
    combined.export(str(output_path), format="wav")

    total_duration = len(combined) / 1000

    print()
    print(f"✅ Combined audio saved!")
    print(f"   File: {output_path}")
    print(f"   Duration: {total_duration:.1f} seconds ({total_duration/60:.1f} minutes)")
    print(f"   Size: {output_path.stat().st_size / 1024:.1f} KB")
    print()

    return output_path


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Prepare and combine voice samples for voice cloning",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process and combine all samples in default directory
  python scripts/prepare_audio.py

  # Process a specific file
  python scripts/prepare_audio.py --input sample.wav

  # Combine samples from specific directory
  python scripts/prepare_audio.py --voice-dir voices/my_voice

  # Process multiple files
  python scripts/prepare_audio.py --process-all
        """
    )

    parser.add_argument(
        "--input", "-i",
        help="Input audio file to process"
    )

    parser.add_argument(
        "--output", "-o",
        help="Output file path"
    )

    parser.add_argument(
        "--voice-dir", "-d",
        default="voices/my_voice",
        help="Voice directory (default: voices/my_voice)"
    )

    parser.add_argument(
        "--process-all", "-a",
        action="store_true",
        help="Process all sample files individually before combining"
    )

    args = parser.parse_args()

    voice_dir = Path(args.voice_dir)

    # Check if voice directory exists
    if not voice_dir.exists():
        print(f"❌ Voice directory not found: {voice_dir}")
        print()
        print("Create it with:")
        print(f"  mkdir -p {voice_dir}")
        print()
        print("Then record samples:")
        print("  python scripts/record_voice.py")
        return

    # Process specific file
    if args.input:
        print("\n📝 Processing single file...")
        print()
        prepare_audio(args.input, args.output)
        return

    # Process all files individually
    if args.process_all:
        print("\n📝 Processing all samples individually...")
        print()

        samples = sorted(glob.glob(str(voice_dir / "sample_*.wav")))

        if not samples:
            print(f"❌ No samples found in {voice_dir}")
            return

        for sample in samples:
            # Skip already processed files
            if ".processed" in sample:
                continue

            prepare_audio(sample)

        print("✅ All samples processed!")
        print()

    # Combine samples
    print("🔗 Combining voice samples...")

    combined_path = combine_samples(voice_dir)

    if combined_path:
        print("✅ Success! Your voice is ready for cloning.")
        print()
        print("Next steps:")
        print("  • Test the voice clone:")
        print(f"    python quick_clone.py \"Hello, this is a test!\"")
        print()
        print("  • Or use the advanced CLI:")
        print("    python cli.py --interactive")
        print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Processing cancelled by user")
        sys.exit(1)
