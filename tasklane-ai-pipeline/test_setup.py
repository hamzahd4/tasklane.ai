#!/usr/bin/env python3
"""
Test script to verify TaskLane Pipeline setup
"""

import sys
import os
from pathlib import Path

def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing module imports...")
    
    try:
        import torch
        print(f"✅ PyTorch: {torch.__version__}")
    except ImportError as e:
        print(f"❌ PyTorch: {e}")
        return False
    
    try:
        import whisperx
        print("✅ WhisperX")
    except ImportError as e:
        print(f"❌ WhisperX: {e}")
        return False
    
    try:
        import ffmpeg
        print("✅ FFmpeg Python")
    except ImportError as e:
        print(f"❌ FFmpeg Python: {e}")
        return False
    
    try:
        from ultralytics import YOLO
        print("✅ Ultralytics (YOLOv8)")
    except ImportError as e:
        print(f"❌ Ultralytics: {e}")
        return False
    
    try:
        from paddleocr import PaddleOCR
        print("✅ PaddleOCR")
    except ImportError as e:
        print(f"❌ PaddleOCR: {e}")
        return False
    
    try:
        from openai import OpenAI
        print("✅ OpenAI")
    except ImportError as e:
        print(f"❌ OpenAI: {e}")
        return False
    
    try:
        from rich.console import Console
        print("✅ Rich")
    except ImportError as e:
        print(f"❌ Rich: {e}")
        return False
    
    return True

def test_ffmpeg_system():
    """Test if FFmpeg is available in system PATH"""
    print("\n🔍 Testing FFmpeg system installation...")
    
    import subprocess
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ FFmpeg system command available")
            return True
        else:
            print("❌ FFmpeg command failed")
            return False
    except FileNotFoundError:
        print("❌ FFmpeg not found in system PATH")
        return False
    except Exception as e:
        print(f"❌ FFmpeg test error: {e}")
        return False

def test_local_modules():
    """Test if our local modules can be imported"""
    print("\n🔍 Testing local modules...")
    
    try:
        from transcription import transcribe_video
        print("✅ transcription.py")
    except ImportError as e:
        print(f"❌ transcription.py: {e}")
        return False
    
    try:
        from frame_extraction import extract_frames
        print("✅ frame_extraction.py")
    except ImportError as e:
        print(f"❌ frame_extraction.py: {e}")
        return False
    
    try:
        from visual_analysis import VisualAnalyzer
        print("✅ visual_analysis.py")
    except ImportError as e:
        print(f"❌ visual_analysis.py: {e}")
        return False
    
    try:
        from sop_generation import SOPGenerator
        print("✅ sop_generation.py")
    except ImportError as e:
        print(f"❌ sop_generation.py: {e}")
        return False
    
    return True

def test_environment():
    """Test environment configuration"""
    print("\n🔍 Testing environment configuration...")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key and api_key != "your_openai_api_key_here":
        print("✅ OpenAI API key configured")
    else:
        print("⚠️ OpenAI API key not configured (will be needed for SOP generation)")
    
    return True

def test_directories():
    """Test if required directories exist"""
    print("\n🔍 Testing directory structure...")
    
    required_dirs = [
        "input_videos",
        "outputs",
        "outputs/transcripts",
        "outputs/frames", 
        "outputs/visual_data",
        "outputs/sops"
    ]
    
    all_exist = True
    for directory in required_dirs:
        if os.path.exists(directory):
            print(f"✅ {directory}/")
        else:
            print(f"❌ {directory}/ (missing)")
            all_exist = False
    
    return all_exist

def main():
    """Run all tests"""
    print("🧪 TaskLane Pipeline Setup Test")
    print("=" * 40)
    
    tests = [
        ("Module Imports", test_imports),
        ("FFmpeg System", test_ffmpeg_system),
        ("Local Modules", test_local_modules),
        ("Environment", test_environment),
        ("Directories", test_directories)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 40)
    print("📊 Test Summary:")
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All tests passed! Your setup is ready.")
        print("\n📋 Next steps:")
        print("1. Add your OpenAI API key to .env file")
        print("2. Place video files in input_videos/ directory")
        print("3. Run: python main.py --video your_video.mp4")
    else:
        print("⚠️ Some tests failed. Please check the setup instructions in README.md")
    
    return passed == len(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 