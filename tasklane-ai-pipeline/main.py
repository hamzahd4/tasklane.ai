#!/usr/bin/env python3
"""
TaskLane AI Pipeline - Video to SOP Converter
Main orchestrator for the complete pipeline
"""

import os
import sys
import json
import argparse
from pathlib import Path
from dotenv import load_dotenv
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel

# Import our modules
from transcription import transcribe_video, get_transcript_text
from frame_extraction import extract_frames, get_frame_timestamp
from visual_analysis import VisualAnalyzer
from sop_generation import SOPGenerator

# Load environment variables
load_dotenv()

# Initialize rich console for better output
console = Console()

class TaskLanePipeline:
    def __init__(self):
        """Initialize the TaskLane pipeline"""
        self.console = Console()
        self.setup_directories()
        
    def setup_directories(self):
        """Create necessary directories if they don't exist"""
        directories = [
            "input_videos",
            "outputs",
            "outputs/transcripts",
            "outputs/frames",
            "outputs/visual_data",
            "outputs/sops"
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
    
    def process_video(self, video_path, output_base_dir="outputs"):
        """
        Process a single video through the complete pipeline
        
        Args:
            video_path (str): Path to the input video file
            output_base_dir (str): Base directory for outputs
        
        Returns:
            dict: Processing results and metadata
        """
        video_name = Path(video_path).stem
        
        self.console.print(Panel(f"[bold blue]🎬 Processing Video: {video_name}[/bold blue]"))
        
        # Step 1: Transcription
        self.console.print("\n[bold green]Step 1: 🎙️ Audio Transcription[/bold green]")
        transcript_dir = os.path.join(output_base_dir, "transcripts")
        transcript_result = transcribe_video(video_path, transcript_dir)
        
        if not transcript_result:
            self.console.print("[red]❌ Transcription failed![/red]")
            return None
        
        # Step 2: Frame Extraction
        self.console.print("\n[bold green]Step 2: 🖼️ Frame Extraction[/bold green]")
        frames_dir = os.path.join(output_base_dir, "frames")
        frame_paths = extract_frames(video_path, frames_dir)
        
        if not frame_paths:
            self.console.print("[red]❌ Frame extraction failed![/red]")
            return None
        
        # Step 3: Visual Analysis
        self.console.print("\n[bold green]Step 3: 🧠 Visual Analysis[/bold green]")
        visual_dir = os.path.join(output_base_dir, "visual_data")
        analyzer = VisualAnalyzer()
        visual_results = analyzer.analyze_frames_batch(frame_paths, visual_dir)
        
        if not visual_results:
            self.console.print("[red]❌ Visual analysis failed![/red]")
            return None
        
        # Step 4: SOP Generation
        self.console.print("\n[bold green]Step 4: 🧾 SOP Generation[/bold green]")
        sop_dir = os.path.join(output_base_dir, "sops")
        sop_generator = SOPGenerator()
        
        sop_text = sop_generator.generate_sop(transcript_result, visual_results, video_name)
        
        if not sop_text:
            self.console.print("[red]❌ SOP generation failed![/red]")
            return None
        
        # Save SOP
        sop_file_path = sop_generator.save_sop(sop_text, sop_dir, video_name)
        
        # Create summary
        summary = {
            "video_name": video_name,
            "video_path": video_path,
            "transcript": {
                "segments_count": len(transcript_result.get("segments", [])),
                "total_text": get_transcript_text(transcript_result)
            },
            "frames": {
                "extracted_count": len(frame_paths),
                "analyzed_count": len(visual_results)
            },
            "visual_analysis": analyzer.get_summary(visual_results),
            "sop": {
                "file_path": sop_file_path,
                "steps_count": len(sop_generator._extract_steps(sop_text))
            }
        }
        
        # Save summary
        summary_path = os.path.join(output_base_dir, f"{video_name}_summary.json")
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2)
        
        self.console.print(f"\n[bold green]✅ Pipeline Complete![/bold green]")
        self.console.print(f"📊 Summary saved to: {summary_path}")
        self.console.print(f"📄 SOP saved to: {sop_file_path}")
        
        return summary
    
    def process_directory(self, input_dir="input_videos", output_dir="outputs"):
        """
        Process all videos in a directory
        
        Args:
            input_dir (str): Directory containing input videos
            output_dir (str): Directory for outputs
        """
        video_extensions = ['.mp4', '.mov', '.webm', '.avi', '.mkv']
        video_files = []
        
        for ext in video_extensions:
            video_files.extend(Path(input_dir).glob(f"*{ext}"))
            video_files.extend(Path(input_dir).glob(f"*{ext.upper()}"))
        
        if not video_files:
            self.console.print(f"[yellow]⚠️ No video files found in {input_dir}[/yellow]")
            return
        
        self.console.print(f"[bold blue]Found {len(video_files)} video(s) to process[/bold blue]")
        
        results = []
        for i, video_file in enumerate(video_files, 1):
            self.console.print(f"\n[bold cyan]Processing {i}/{len(video_files)}: {video_file.name}[/bold cyan]")
            
            try:
                result = self.process_video(str(video_file), output_dir)
                if result:
                    results.append(result)
            except Exception as e:
                self.console.print(f"[red]❌ Error processing {video_file.name}: {e}[/red]")
        
        self.console.print(f"\n[bold green]🎉 Batch processing complete! {len(results)}/{len(video_files)} videos processed successfully.[/bold green]")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="TaskLane AI Pipeline - Video to SOP Converter")
    parser.add_argument("--video", "-v", help="Path to single video file")
    parser.add_argument("--input-dir", "-i", default="input_videos", help="Input directory for videos")
    parser.add_argument("--output-dir", "-o", default="outputs", help="Output directory")
    parser.add_argument("--check-setup", action="store_true", help="Check if all dependencies are installed")
    
    args = parser.parse_args()
    
    # Check setup if requested
    if args.check_setup:
        check_setup()
        return
    
    # Initialize pipeline
    pipeline = TaskLanePipeline()
    
    # Process video(s)
    if args.video:
        if not os.path.exists(args.video):
            console.print(f"[red]❌ Video file not found: {args.video}[/red]")
            return
        pipeline.process_video(args.video, args.output_dir)
    else:
        pipeline.process_directory(args.input_dir, args.output_dir)

def check_setup():
    """Check if all dependencies and setup are correct"""
    console.print("[bold blue]🔍 Checking TaskLane Pipeline Setup[/bold blue]")
    
    # Check Python version
    python_version = sys.version_info
    console.print(f"🐍 Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version < (3, 8):
        console.print("[red]❌ Python 3.8+ required[/red]")
    else:
        console.print("[green]✅ Python version OK[/green]")
    
    # Check environment variables
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key and api_key != "your_openai_api_key_here":
        console.print("[green]✅ OpenAI API key configured[/green]")
    else:
        console.print("[yellow]⚠️ OpenAI API key not configured[/yellow]")
    
    # Check directories
    required_dirs = ["input_videos", "outputs"]
    for directory in required_dirs:
        if os.path.exists(directory):
            console.print(f"[green]✅ Directory exists: {directory}[/green]")
        else:
            console.print(f"[yellow]⚠️ Directory missing: {directory}[/yellow]")
    
    # Check for video files
    video_files = list(Path("input_videos").glob("*.mp4")) + list(Path("input_videos").glob("*.mov"))
    if video_files:
        console.print(f"[green]✅ Found {len(video_files)} video file(s) in input_videos/[/green]")
    else:
        console.print("[yellow]⚠️ No video files found in input_videos/[/yellow]")
    
    console.print("\n[bold blue]📋 Setup Instructions:[/bold blue]")
    console.print("1. Install Python 3.8+")
    console.print("2. Install FFmpeg and add to PATH")
    console.print("3. Copy env_template.txt to .env and add your OpenAI API key")
    console.print("4. Install dependencies: pip install -r requirements.txt")
    console.print("5. Place video files in input_videos/ directory")

if __name__ == "__main__":
    main() 