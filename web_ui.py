#!/usr/bin/env python3
"""
Voice Cloning Web UI
Browser-based interface using Gradio
"""

import gradio as gr
from pathlib import Path
import sys
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.voice_cloner import VoiceCloner, validate_path


def list_voice_files():
    """
    Get list of available voice files

    Returns:
        List of (display_name, file_path) tuples
    """
    voices_dir = Path("voices")
    voice_files = []

    if not voices_dir.exists():
        return []

    for voice_dir in sorted(voices_dir.iterdir()):
        if voice_dir.is_dir() and not voice_dir.name.startswith("."):
            # Look for combined.wav first
            combined = voice_dir / "combined.wav"
            if combined.exists():
                voice_files.append((f"{voice_dir.name}/combined.wav", str(combined)))

            # Also add individual samples
            for wav_file in sorted(voice_dir.glob("sample_*.wav")):
                display_name = f"{voice_dir.name}/{wav_file.name}"
                voice_files.append((display_name, str(wav_file)))

    return voice_files


def create_web_ui():
    """Create and configure Gradio web interface"""

    # Initialize voice cloner (loaded once at startup)
    print("🎙️  Initializing Voice Cloning Web UI...")
    print()

    try:
        cloner = VoiceCloner()
    except Exception as e:
        print(f"❌ Error initializing voice cloner: {e}")
        print()
        print("Make sure dependencies are installed:")
        print("  pip install -r requirements.txt")
        return None

    print("✅ Voice cloner ready!")
    print()

    def generate_speech(text, voice_file, language):
        """
        Generate cloned speech from text

        Args:
            text: Text to synthesize
            voice_file: Path to voice reference file
            language: Language code

        Returns:
            (audio_path, status_message) tuple
        """
        # Validate inputs
        MAX_TEXT_LENGTH = 10000

        if not text or not text.strip():
            return None, "❌ Error: Please enter some text to synthesize"

        if len(text) > MAX_TEXT_LENGTH:
            return None, f"❌ Error: Text too long (max {MAX_TEXT_LENGTH} characters)"

        if not voice_file:
            return None, "❌ Error: Please select a voice file"

        # Validate voice file path
        try:
            voice_path = validate_path(voice_file, "voices")
            if not voice_path.exists():
                return None, f"❌ Error: Voice file not found: {voice_file}"
        except ValueError as e:
            return None, f"❌ Error: {e}"

        # Create output directory
        output_dir = Path("outputs")
        output_dir.mkdir(exist_ok=True)

        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = output_dir / f"web_ui_{timestamp}.wav"

        # Generate speech
        try:
            cloner.clone_voice(
                text=text,
                reference_audio=voice_file,
                output_path=str(output_path),
                language=language
            )

            size_kb = output_path.stat().st_size / 1024
            return str(output_path), f"✅ Generated successfully! ({size_kb:.1f} KB)"

        except Exception as e:
            return None, f"❌ Error: {str(e)}"

    def refresh_voices():
        """Refresh the list of available voices"""
        voice_files = list_voice_files()
        if voice_files:
            choices = [display for display, path in voice_files]
            values = [path for display, path in voice_files]
            return gr.Dropdown(choices=list(zip(choices, values)), value=values[0] if values else None)
        else:
            return gr.Dropdown(choices=[], value=None)

    # Get initial voice files
    voice_files = list_voice_files()
    voice_choices = [(display, path) for display, path in voice_files]
    default_voice = voice_files[0][1] if voice_files else None

    # Supported languages
    languages = cloner.get_supported_languages()
    language_names = {
        "en": "English",
        "es": "Spanish (Español)",
        "fr": "French (Français)",
        "de": "German (Deutsch)",
        "it": "Italian (Italiano)",
        "pt": "Portuguese (Português)",
        "pl": "Polish (Polski)",
        "tr": "Turkish (Türkçe)",
        "ru": "Russian (Русский)",
        "nl": "Dutch (Nederlands)",
        "cs": "Czech (Čeština)",
        "ar": "Arabic (العربية)",
        "zh-cn": "Chinese (中文)",
        "ja": "Japanese (日本語)",
        "hu": "Hungarian (Magyar)",
        "ko": "Korean (한국어)"
    }

    language_choices = [(language_names.get(lang, lang), lang) for lang in languages]

    # Create Gradio interface
    with gr.Blocks(
        title="Voice Cloning Studio",
        theme=gr.themes.Soft()
    ) as app:
        gr.Markdown(
            """
            # 🎙️ Voice Cloning Studio
            Clone your voice and generate speech from text using AI
            """
        )

        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### Input")

                text_input = gr.Textbox(
                    label="Text to Synthesize",
                    placeholder="Enter the text you want to hear in the cloned voice...",
                    lines=6,
                    max_lines=10
                )

                voice_dropdown = gr.Dropdown(
                    label="Voice Reference",
                    choices=voice_choices,
                    value=default_voice,
                    interactive=True
                )

                refresh_btn = gr.Button("🔄 Refresh Voices", size="sm")

                language_dropdown = gr.Dropdown(
                    label="Language",
                    choices=language_choices,
                    value="en",
                    interactive=True
                )

                generate_btn = gr.Button(
                    "🎤 Generate Speech",
                    variant="primary",
                    size="lg"
                )

            with gr.Column(scale=1):
                gr.Markdown("### Output")

                audio_output = gr.Audio(
                    label="Generated Audio",
                    type="filepath",
                    interactive=False
                )

                status_text = gr.Textbox(
                    label="Status",
                    interactive=False,
                    lines=2
                )

        # Info section
        with gr.Accordion("ℹ️ Tips & Information", open=False):
            gr.Markdown(
                """
                ### Tips for Best Results:
                - **Clear text**: Use proper punctuation and grammar
                - **Voice reference**: Use 30 seconds to 5 minutes of clean audio
                - **Language**: Select the language matching your text
                - **Quality**: Reference audio should be noise-free

                ### First Time Setup:
                1. Record your voice: `python scripts/record_voice.py 120`
                2. Prepare audio: `python scripts/prepare_audio.py`
                3. Refresh voices (click button above)
                4. Start generating!

                ### Technical Details:
                - **Model**: Coqui TTS XTTS-v2 (zero-shot voice cloning)
                - **GPU Acceleration**: Automatically enabled if available
                - **Languages**: 17+ supported languages
                - **Speed**: ~5-10 seconds per sentence on GPU

                ### Troubleshooting:
                - **No voices available**: Record and prepare voice samples first
                - **Poor quality**: Use cleaner reference audio or longer samples
                - **Slow generation**: First run downloads model (~2GB)
                """
            )

        # Event handlers
        generate_btn.click(
            fn=generate_speech,
            inputs=[text_input, voice_dropdown, language_dropdown],
            outputs=[audio_output, status_text]
        )

        refresh_btn.click(
            fn=lambda: gr.Dropdown(
                choices=[(display, path) for display, path in list_voice_files()],
                value=list_voice_files()[0][1] if list_voice_files() else None
            ),
            outputs=[voice_dropdown]
        )

        # Example inputs
        gr.Examples(
            examples=[
                ["Hello world, this is my cloned voice speaking!"],
                ["What a beautiful day it is today!"],
                ["I'm testing this amazing voice cloning technology."],
                ["The quick brown fox jumps over the lazy dog."]
            ],
            inputs=[text_input]
        )

    return app


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="Voice Cloning Web UI")

    parser.add_argument(
        "--port", "-p",
        type=int,
        default=7860,
        help="Port to run server on (default: 7860)"
    )

    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host to bind to (default: 127.0.0.1)"
    )

    parser.add_argument(
        "--share",
        action="store_true",
        help="Create public share link (for remote access)"
    )

    parser.add_argument(
        "--auth",
        nargs=2,
        metavar=("USERNAME", "PASSWORD"),
        help="Enable basic authentication (username password)"
    )

    args = parser.parse_args()

    # Check if voices exist
    voices_dir = Path("voices")
    voice_files = list_voice_files()

    if not voice_files:
        print("⚠️  Warning: No voice files found!")
        print()
        print("Create voice samples first:")
        print("  1. python scripts/record_voice.py 120")
        print("  2. python scripts/prepare_audio.py")
        print()
        print("Continuing anyway (you can record later)...")
        print()

    # Create and launch UI
    app = create_web_ui()

    if app is None:
        print("❌ Failed to initialize web UI")
        sys.exit(1)

    print("=" * 60)
    print("🚀 Launching Voice Cloning Web UI")
    print("=" * 60)
    print()
    print(f"🌐 Local URL: http://{args.host}:{args.port}")
    if args.share:
        print("🌍 Public URL will be generated...")
    if args.auth:
        print(f"🔒 Authentication enabled for user: {args.auth[0]}")
    print()
    print("Press Ctrl+C to stop the server")
    print()

    # Prepare authentication tuple
    auth_tuple = tuple(args.auth) if args.auth else None

    app.launch(
        server_name=args.host,
        server_port=args.port,
        share=args.share,
        auth=auth_tuple,
        inbrowser=True  # Auto-open browser
    )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped")
        sys.exit(0)
