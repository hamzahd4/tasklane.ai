import whisperx
import os
import json
from dotenv import load_dotenv

load_dotenv()

def transcribe_video(filepath, output_dir):
    """
    Transcribe video file using WhisperX
    
    Args:
        filepath (str): Path to the input video file
        output_dir (str): Directory to save transcript output
    
    Returns:
        dict: Transcription result with timestamps
    """
    print(f"🔄 Starting transcription for: {filepath}")
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Load WhisperX model
    model_name = os.getenv("WHISPER_MODEL", "medium")
    device = os.getenv("DEVICE", "cuda")
    
    print(f"📥 Loading WhisperX model: {model_name}")
    model = whisperx.load_model(model_name, device=device)
    
    # Load audio from video
    print("🎵 Extracting audio from video...")
    audio = whisperx.load_audio(filepath)
    
    # Transcribe audio
    print("🎙️ Transcribing audio...")
    result = model.transcribe(audio)
    
    # Save transcript to JSON
    output_path = os.path.join(output_dir, "transcript.json")
    whisperx.save_json(result, output_path)
    
    print(f"✅ Transcription saved to: {output_path}")
    
    return result

def get_transcript_text(transcript_result):
    """
    Extract plain text from transcript result
    
    Args:
        transcript_result (dict): WhisperX transcription result
    
    Returns:
        str: Plain text transcript
    """
    if "segments" in transcript_result:
        return " ".join([segment["text"] for segment in transcript_result["segments"]])
    return transcript_result.get("text", "") 