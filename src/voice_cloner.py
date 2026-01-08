"""
Voice Cloning Module
Core functionality for local AI voice cloning using Coqui TTS XTTS-v2
"""

import torch
from TTS.api import TTS
import os
from pathlib import Path


def validate_path(path, allowed_parent):
    """
    Validate that a path is within an allowed directory

    Prevents path traversal attacks by ensuring the resolved path
    is within the allowed parent directory.

    Args:
        path: Path to validate (can be relative or absolute)
        allowed_parent: Parent directory that path must be within

    Returns:
        Resolved Path object if valid

    Raises:
        ValueError: If path is outside allowed directory
    """
    try:
        resolved = Path(path).resolve()
        allowed = Path(allowed_parent).resolve()
        resolved.relative_to(allowed)
        return resolved
    except (ValueError, RuntimeError) as e:
        raise ValueError(f"Invalid path: {path} (must be within {allowed_parent})")


class VoiceCloner:
    """
    Voice cloning system using XTTS-v2 model

    Features:
    - Zero-shot voice cloning (no training required)
    - GPU acceleration with CUDA support
    - Multi-language support (17+ languages)
    - High quality output
    """

    def __init__(self, model_name="tts_models/multilingual/multi-dataset/xtts_v2"):
        """
        Initialize voice cloning system

        Args:
            model_name: TTS model to use (default: XTTS-v2)
        """
        # Detect device (CUDA GPU or CPU)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"🎙️  Voice Cloner initialized")
        print(f"📱 Device: {self.device.upper()}")

        if self.device == "cuda":
            gpu_name = torch.cuda.get_device_name(0)
            gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1024**3
            print(f"🎮 GPU: {gpu_name} ({gpu_memory:.1f} GB)")

        # Initialize TTS model
        print(f"📦 Loading {model_name}...")
        print("   (First run will download ~2GB model)")

        self.tts = TTS(model_name).to(self.device)

        print("✅ Model loaded successfully!")
        print()

    def clone_voice(self, text, reference_audio, output_path, language="en"):
        """
        Clone voice and generate speech

        Args:
            text: Text to synthesize
            reference_audio: Path to reference voice audio (6 seconds - 5 minutes)
            output_path: Where to save generated audio
            language: Language code (en, es, fr, de, it, pt, pl, tr, ru, nl, cs, ar, zh-cn, ja, hu, ko)

        Returns:
            Path to generated audio file
        """
        # Validate inputs
        if not os.path.exists(reference_audio):
            raise FileNotFoundError(f"Reference audio not found: {reference_audio}")

        if not text or not text.strip():
            raise ValueError("Text cannot be empty")

        # Create output directory if needed
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        # Display generation info
        text_preview = text[:60] + "..." if len(text) > 60 else text
        print(f"🎤 Generating: '{text_preview}'")
        print(f"🔊 Reference: {Path(reference_audio).name}")
        print(f"🌍 Language: {language}")
        print(f"⏳ Processing...")

        # Generate audio
        try:
            self.tts.tts_to_file(
                text=text,
                file_path=output_path,
                speaker_wav=reference_audio,
                language=language
            )

            print(f"✅ Audio saved to: {output_path}")
            print()

            return output_path

        except Exception as e:
            print(f"❌ Error generating audio: {e}")
            raise

    def clone_voice_streaming(self, text, reference_audio, language="en"):
        """
        Generate audio and return as numpy array for immediate playback

        Args:
            text: Text to synthesize
            reference_audio: Path to reference voice audio
            language: Language code

        Returns:
            numpy array of audio samples
        """
        if not os.path.exists(reference_audio):
            raise FileNotFoundError(f"Reference audio not found: {reference_audio}")

        wav = self.tts.tts(
            text=text,
            speaker_wav=reference_audio,
            language=language
        )

        return wav

    def get_supported_languages(self):
        """
        Get list of supported languages

        Returns:
            List of language codes
        """
        return ["en", "es", "fr", "de", "it", "pt", "pl", "tr",
                "ru", "nl", "cs", "ar", "zh-cn", "ja", "hu", "ko"]


# Example usage / testing
if __name__ == "__main__":
    import sys

    print("=== Voice Cloner Test ===")
    print()

    # Initialize cloner
    cloner = VoiceCloner()

    # Test with dummy data
    test_text = "Hello, this is a test of the voice cloning system!"
    test_voice = "voices/my_voice/combined.wav"
    test_output = "outputs/test_output.wav"

    if os.path.exists(test_voice):
        print("Running test generation...")
        cloner.clone_voice(
            text=test_text,
            reference_audio=test_voice,
            output_path=test_output
        )
        print(f"Test complete! Check {test_output}")
    else:
        print(f"⚠️  No voice file found at: {test_voice}")
        print("   Record your voice first using: python scripts/record_voice.py")
        print()
        print("Supported languages:", ", ".join(cloner.get_supported_languages()))
