#!/usr/bin/env python3
"""
Example script demonstrating TaskLane Pipeline usage
"""

import os
import json
from pathlib import Path
from dotenv import load_dotenv

# Import our modules
from transcription import transcribe_video, get_transcript_text
from frame_extraction import extract_frames
from visual_analysis import VisualAnalyzer
from sop_generation import SOPGenerator

def create_sample_data():
    """Create sample data for demonstration"""
    print("📝 Creating sample data for demonstration...")
    
    # Sample transcript data (simulating WhisperX output)
    sample_transcript = {
        "segments": [
            {
                "start": 0.0,
                "end": 3.0,
                "text": "First, open your web browser and navigate to the settings page."
            },
            {
                "start": 3.0,
                "end": 6.0,
                "text": "Look for the privacy section in the left sidebar."
            },
            {
                "start": 6.0,
                "end": 9.0,
                "text": "Click on the clear browsing data option."
            },
            {
                "start": 9.0,
                "end": 12.0,
                "text": "Select the time range you want to clear."
            },
            {
                "start": 12.0,
                "end": 15.0,
                "text": "Finally, click the clear data button to complete the process."
            }
        ],
        "text": "First, open your web browser and navigate to the settings page. Look for the privacy section in the left sidebar. Click on the clear browsing data option. Select the time range you want to clear. Finally, click the clear data button to complete the process."
    }
    
    # Sample visual analysis data (simulating YOLO + OCR output)
    sample_visual_data = [
        {
            "frame": "frame_0001.png",
            "yolo_detections": [
                {
                    "class_name": "computer",
                    "confidence": 0.95,
                    "bbox": [100, 100, 300, 400]
                },
                {
                    "class_name": "mouse",
                    "confidence": 0.87,
                    "bbox": [350, 200, 380, 230]
                }
            ],
            "ocr_text": [
                {
                    "text": "Settings",
                    "confidence": 0.92,
                    "bbox": [[150, 50], [250, 50], [250, 80], [150, 80]]
                }
            ],
            "objects_count": 2,
            "text_count": 1
        },
        {
            "frame": "frame_0002.png",
            "yolo_detections": [
                {
                    "class_name": "computer",
                    "confidence": 0.94,
                    "bbox": [100, 100, 300, 400]
                }
            ],
            "ocr_text": [
                {
                    "text": "Privacy",
                    "confidence": 0.89,
                    "bbox": [[120, 150], [200, 150], [200, 180], [120, 180]]
                },
                {
                    "text": "Clear browsing data",
                    "confidence": 0.85,
                    "bbox": [[120, 200], [280, 200], [280, 230], [120, 230]]
                }
            ],
            "objects_count": 1,
            "text_count": 2
        }
    ]
    
    return sample_transcript, sample_visual_data

def demonstrate_pipeline():
    """Demonstrate the complete pipeline with sample data"""
    print("🎬 TaskLane Pipeline Demonstration")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Create sample data
    transcript_data, visual_data = create_sample_data()
    
    print("\n📊 Sample Data Created:")
    print(f"  - Transcript segments: {len(transcript_data['segments'])}")
    print(f"  - Visual frames: {len(visual_data)}")
    
    # Step 1: Show transcript
    print("\n🎙️ Step 1: Audio Transcription")
    print("-" * 30)
    transcript_text = get_transcript_text(transcript_data)
    print(f"Transcript: {transcript_text}")
    
    # Step 2: Show visual analysis
    print("\n🧠 Step 2: Visual Analysis")
    print("-" * 30)
    analyzer = VisualAnalyzer()
    summary = analyzer.get_summary(visual_data)
    print(f"Objects detected: {summary['unique_object_classes']}")
    print(f"Text detected: {summary['detected_text']}")
    
    # Step 3: Generate SOP
    print("\n🧾 Step 3: SOP Generation")
    print("-" * 30)
    
    try:
        sop_generator = SOPGenerator()
        sop_text = sop_generator.generate_sop(transcript_data, visual_data, "demo_video")
        
        if sop_text:
            print("Generated SOP:")
            print(sop_text)
            
            # Save SOP
            sop_file = sop_generator.save_sop(sop_text, "outputs/sops", "demo_video")
            print(f"\n💾 SOP saved to: {sop_file}")
        else:
            print("⚠️ SOP generation failed (likely due to missing OpenAI API key)")
            print("This is expected in demo mode without API key")
            
    except Exception as e:
        print(f"⚠️ SOP generation error: {e}")
        print("This is expected if OpenAI API key is not configured")
    
    print("\n✅ Demonstration complete!")
    print("\n📋 To run with real data:")
    print("1. Add your OpenAI API key to .env file")
    print("2. Place video files in input_videos/ directory")
    print("3. Run: python main.py --video your_video.mp4")

def demonstrate_individual_modules():
    """Demonstrate individual module functionality"""
    print("\n🔧 Individual Module Demonstration")
    print("=" * 50)
    
    # Test transcription module
    print("\n🎙️ Transcription Module Test")
    print("-" * 30)
    sample_transcript = {
        "segments": [
            {"text": "Hello world", "start": 0, "end": 1},
            {"text": "This is a test", "start": 1, "end": 2}
        ]
    }
    text = get_transcript_text(sample_transcript)
    print(f"Extracted text: {text}")
    
    # Test visual analysis module
    print("\n🧠 Visual Analysis Module Test")
    print("-" * 30)
    try:
        analyzer = VisualAnalyzer()
        print("✅ VisualAnalyzer initialized successfully")
    except Exception as e:
        print(f"⚠️ VisualAnalyzer initialization: {e}")
    
    # Test frame extraction module
    print("\n🖼️ Frame Extraction Module Test")
    print("-" * 30)
    fps = 1
    print(f"Frame extraction configured for {fps} FPS")
    
    print("\n✅ Individual module tests complete!")

if __name__ == "__main__":
    print("🚀 TaskLane Pipeline Example")
    print("This script demonstrates the pipeline functionality")
    
    # Demonstrate individual modules
    demonstrate_individual_modules()
    
    # Demonstrate complete pipeline
    demonstrate_pipeline()
    
    print("\n🎉 Example completed successfully!")
    print("Check the outputs/ directory for generated files.") 