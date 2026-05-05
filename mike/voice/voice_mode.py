"""
Voice input mode for Mike

Uses Whisper for speech recognition and system TTS for output.
"""

import sys
import os
import tempfile
import subprocess
from pathlib import Path

import numpy as np
import sounddevice as sd

from rich.console import Console
from rich.panel import Panel

console = Console()


def resample_audio(audio: np.ndarray, orig_sr: int, target_sr: int) -> np.ndarray:
    """Resample audio data to target sample rate."""
    if orig_sr == target_sr:
        return audio

    import numpy as np
    duration = len(audio) / orig_sr
    num_samples = int(duration * target_sr)
    return np.interp(
        np.linspace(0, duration, num_samples),
        np.linspace(0, duration, len(audio)),
        audio
    ).astype(np.float32)


def list_audio_devices():
    """List available audio input devices."""
    try:
        import sounddevice as sd
        devices = sd.query_devices()
        default_input = sd.default.device[0]

        console.print("\n[bold blue]Available Audio Input Devices:[/bold blue]")
        console.print("-" * 60)

        for i, device in enumerate(devices):
            if device['max_input_channels'] > 0:
                prefix = ""
                if i == default_input:
                    prefix += "[bold green](Default)[/bold green] "

                console.print(f"{i}: {prefix}{device['name']}")
                console.print(f"   Channels: {device['max_input_channels']} | Sample Rate: {device['default_samplerate']}Hz")
        console.print()
    except Exception as e:
        console.print(f"[red]Error listing devices: {e}[/red]")
def run_voice_mode(device_id: int = None):
    """Run Mike in voice input mode."""
    # Check dependencies
    try:
        import whisper
    except ImportError as e:
        console.print(f"[red]Missing dependency: {e}[/red]")
        console.print("Install with: pip install mike-ai-assistant[voice]")
        sys.exit(1)

    from ..assistant import Mike, load_config

    # Load preferred device from config if not provided
    if device_id is None:
        config = load_config()
        device_id = config.get("voice", {}).get("input_device")

    console.print(Panel.fit(
        "[bold blue]MIKE[/bold blue] - Voice Mode\n"
        "[dim]Press Enter to speak, Ctrl+C to exit[/dim]",
        border_style="blue"
    ))

    # Show current device
    try:
        if device_id is not None:
            device_info = sd.query_devices(device_id)
            sd.default.device = (device_id, sd.default.device[1])
        else:
            device_id = sd.default.device[0]
            device_info = sd.query_devices(device_id)

        console.print(f"[cyan]🎤 Using Microphone:[/cyan] [bold]{device_info['name']}[/bold] (ID: {device_id})")
    except Exception as e:
        console.print(f"[yellow]Warning: Could not set preferred device {device_id}: {e}[/yellow]")
        console.print(f"[dim]Falling back to system default.[/dim]")

    # Load Whisper model
    console.print("[dim]Loading Whisper model...[/dim]")
    model = whisper.load_model("base")  # Options: tiny, base, small, medium, large
    console.print("[green]✓ Whisper loaded[/green]")

    # Initialize Mike
    try:
        mike = Mike()
    except Exception as e:
        console.print(f"[red]Failed to initialize: {e}[/red]")
        sys.exit(1)

    # Use current persona and model info
    persona = getattr(mike, 'current_persona', 'default')
    model_name = getattr(mike.provider, 'model', 'unknown')
    console.print(f"[dim]Persona: {persona} | Model: {model_name}[/dim]\n")

    # Audio settings - record at device's native rate and resample to 16kHz for Whisper
    target_sample_rate = 16000
    try:
        device_info = sd.query_devices(device_id, 'input')
        device_sample_rate = int(device_info['default_samplerate'])
        channels = min(device_info['max_input_channels'], 1)  # Try to use mono if possible
    except Exception:
        device_sample_rate = 16000
        channels = 1

    duration = 5  # seconds to record

    while True:
        try:
            input("\n[Press Enter to speak, then talk for 5 seconds...]")
            console.print("[cyan]🎤 Listening...[/cyan]")

            # Record audio at device's native rate
            audio = sd.rec(
                int(duration * device_sample_rate),
                samplerate=device_sample_rate,
                channels=channels,
                device=device_id,
                dtype=np.float32
            )
            sd.wait()

            console.print("[dim]Processing speech...[/dim]")

            # Transcribe with Whisper
            audio_data = audio.flatten()

            # Resample if necessary
            if device_sample_rate != target_sample_rate:
                audio_data = resample_audio(audio_data, device_sample_rate, target_sample_rate)

            result = model.transcribe(audio_data, fp16=False)
            text = result["text"].strip()

            if not text:
                console.print("[yellow]No speech detected. Try again.[/yellow]")
                continue

            console.print(f"\n[bold green]You said:[/bold green] {text}")

            # Check for exit commands
            if text.lower() in ["exit", "quit", "goodbye", "bye"]:
                speak("Goodbye!")
                console.print("[yellow]Goodbye![/yellow]")
                break

            # Process with Mike
            console.print("\n[bold blue]Mike:[/bold blue]", end=" ")
            response = mike.process(text)

            # Speak the response (if not too long)
            if len(response) < 500:
                speak(response)

        except KeyboardInterrupt:
            console.print("\n[yellow]Goodbye![/yellow]")
            break
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")


def speak(text: str):
    """Use system TTS to speak text."""
    if sys.platform == "darwin":
        # macOS: use 'say' command
        subprocess.run(["say", text], capture_output=True)
    elif sys.platform == "linux":
        # Linux: try espeak
        try:
            subprocess.run(["espeak", text], capture_output=True)
        except FileNotFoundError:
            pass  # espeak not installed
    # Windows: could use pyttsx3 or powershell


def record_audio_continuous(sample_rate: int = 16000, silence_threshold: float = 0.01,
                            silence_duration: float = 1.5, max_duration: float = 30.0):
    """
    Record audio until silence is detected.

    Args:
        sample_rate: Audio sample rate
        silence_threshold: RMS threshold for silence
        silence_duration: Seconds of silence to stop recording
        max_duration: Maximum recording duration

    Returns:
        numpy array of audio data
    """
    import numpy as np
    import sounddevice as sd

    console.print("[cyan]🎤 Listening... (speak now, will stop on silence)[/cyan]")

    chunk_duration = 0.1  # seconds per chunk
    chunk_samples = int(sample_rate * chunk_duration)
    silence_chunks = int(silence_duration / chunk_duration)
    max_chunks = int(max_duration / chunk_duration)

    audio_chunks = []
    silent_count = 0
    has_speech = False

    for _ in range(max_chunks):
        chunk = sd.rec(chunk_samples, samplerate=sample_rate, channels=1, dtype=np.float32)
        sd.wait()

        rms = np.sqrt(np.mean(chunk**2))
        audio_chunks.append(chunk)

        if rms > silence_threshold:
            has_speech = True
            silent_count = 0
        else:
            silent_count += 1

        # Stop if we've had speech and then silence
        if has_speech and silent_count >= silence_chunks:
            break

    return np.concatenate(audio_chunks).flatten() if audio_chunks else np.array([])


if __name__ == "__main__":
    run_voice_mode()
