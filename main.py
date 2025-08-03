from dotenv import load_dotenv
import os
import json
 
from modules.transcription import transcribe_video
from modules.frame_extraction import extract_frames
from modules.visual_analysis import analyze_frame
from modules.sop_generation import generate_sop
 
load_dotenv()
 
def main():
    video_path = "input_videos/demo.mp4"
    os.makedirs("outputs/transcripts", exist_ok=True)
    os.makedirs("outputs/frames", exist_ok=True)
    os.makedirs("outputs/visual_data", exist_ok=True)
    os.makedirs("outputs/sops", exist_ok=True)
 
    print("[1/5] Transcribing video...")
    transcript = transcribe_video(video_path, "outputs/transcripts")
 
    print("[2/5] Extracting frames...")
    extract_frames(video_path, "outputs/frames", fps=1)
 
    print("[3/5] Analyzing frames...")
    visual_output = []
    frame_files = sorted(os.listdir("outputs/frames"))
    for frame_file in frame_files:
        yolo_results, ocr_results = analyze_frame(f"outputs/frames/{frame_file}")
        visual_output.append({
            "frame": frame_file,
            "yolo": yolo_results,
            "ocr": ocr_results,
        })
 
    print("[4/5] Generating SOP...")
    sop_text = generate_sop(json.dumps(transcript), json.dumps(visual_output))
 
    output_path = "outputs/sops/demo_sop.txt"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(sop_text)
 
    print(f"[5/5] SOP saved to {output_path}")
 
if __name__ == "__main__":
    main()