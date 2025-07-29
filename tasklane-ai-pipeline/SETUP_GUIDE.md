# TaskLane AI Pipeline - Setup Guide 🚀

## Quick Setup Checklist

- [ ] Install Python 3.8+
- [ ] Install FFmpeg
- [ ] Get OpenAI API key
- [ ] Clone/download project
- [ ] Create virtual environment
- [ ] Install dependencies
- [ ] Configure environment
- [ ] Test setup
- [ ] Add video files
- [ ] Run pipeline

## Detailed Setup Instructions

### 1. Install Python 3.8+

**Windows:**
1. Download from [python.org](https://www.python.org/downloads/)
2. Run installer with "Add to PATH" checked
3. Verify: `python --version`

**macOS:**
```bash
brew install python
```

**Linux:**
```bash
sudo apt update
sudo apt install python3 python3-pip
```

### 2. Install FFmpeg

**Windows:**
1. Download from [ffmpeg.org](https://ffmpeg.org/download.html)
2. Extract to `C:\ffmpeg`
3. Add `C:\ffmpeg\bin` to system PATH
4. Verify: `ffmpeg -version`

**macOS:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt install ffmpeg
```

### 3. Get OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign up/login
3. Create new API key
4. Copy the key (starts with `sk-`)

### 4. Project Setup

**Option A: Using the batch script (Windows)**
```bash
# Double-click run_pipeline.bat
# Or run from command line:
run_pipeline.bat
```

**Option B: Manual setup**
```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
copy env_template.txt .env
# Edit .env file with your OpenAI API key

# 5. Test setup
python test_setup.py
```

### 5. Configuration

Edit the `.env` file:
```bash
# Required
OPENAI_API_KEY=sk-your-actual-api-key-here

# Optional (defaults shown)
WHISPER_MODEL=medium
YOLO_MODEL=yolov8n.pt
DEVICE=cuda
FRAME_EXTRACTION_FPS=1
```

### 6. Test Your Setup

```bash
# Run comprehensive test
python test_setup.py

# Or use the built-in check
python main.py --check-setup
```

### 7. Add Your Videos

Place video files in the `input_videos/` directory:
- Supported formats: `.mp4`, `.mov`, `.webm`, `.avi`, `.mkv`
- Recommended: Short instructional videos (1-10 minutes)

### 8. Run the Pipeline

**Process all videos in directory:**
```bash
python main.py
```

**Process single video:**
```bash
python main.py --video "input_videos/your_video.mp4"
```

**Check available options:**
```bash
python main.py --help
```

## Troubleshooting

### Common Issues

**1. "Python not found"**
- Install Python and add to PATH
- Use `py` instead of `python` on Windows

**2. "FFmpeg not found"**
- Install FFmpeg and add to system PATH
- Restart terminal after adding to PATH

**3. "CUDA/GPU errors"**
- Set `DEVICE=cpu` in `.env` file
- Install CPU-only PyTorch: `pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu`

**4. "OpenAI API errors"**
- Verify API key in `.env` file
- Check API quota and billing
- Ensure key starts with `sk-`

**5. "Memory issues"**
- Use smaller models (WhisperX small, YOLOv8n)
- Reduce `FRAME_EXTRACTION_FPS` in `.env`
- Process shorter videos

**6. "Module import errors"**
- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`
- Check Python version (3.8+ required)

### Performance Optimization

**For faster processing:**
- Use GPU (CUDA) if available
- Use smaller models for quick testing
- Reduce frame extraction FPS
- Process videos in smaller batches

**For better accuracy:**
- Use larger models (WhisperX large, YOLOv8x)
- Increase frame extraction FPS
- Ensure good video quality

## Example Workflow

1. **Prepare your video**
   - Clear audio narration
   - Good visual quality
   - Instructional content

2. **Run the pipeline**
   ```bash
   python main.py --video "input_videos/tutorial.mp4"
   ```

3. **Check outputs**
   - `outputs/transcripts/` - Audio transcription
   - `outputs/frames/` - Extracted video frames
   - `outputs/visual_data/` - Object and text detection
   - `outputs/sops/` - Generated SOP files

4. **Review and refine**
   - Check generated SOP for accuracy
   - Edit if needed
   - Use for training or documentation

## Support

If you encounter issues:

1. **Check the troubleshooting section above**
2. **Run the test script**: `python test_setup.py`
3. **Check the logs** for specific error messages
4. **Verify your setup** with `python main.py --check-setup`

## Next Steps

After successful setup:

1. **Try the example**: `python example.py`
2. **Process your first video**
3. **Customize the pipeline** for your needs
4. **Scale up** for batch processing
5. **Integrate** with your existing workflows

---

**Happy SOP generation! 🎉** 