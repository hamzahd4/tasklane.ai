import whisper
import os
import json

def transcribe_video(filepath, output_dir):
    # Load the Whisper model (medium size, adjust as needed)
    model = whisper.load_model("medium")

    # Transcribe the audio from the video file
    result = model.transcribe(filepath)

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Save result as JSON
    output_path = os.path.join(output_dir, "transcript.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=4)

    return result


if __name__ == "__main__":
    filepath = "input_videos/sample_video.mp4"
    output_dir = "outputs/transcription"
    transcribe_video(filepath, output_dir)
