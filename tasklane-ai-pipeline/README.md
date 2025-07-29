# TaskLane AI Pipeline 🎬➡️📋

**Automated Video-to-SOP Converter using AI**

Transform instructional videos into structured Standard Operating Procedures (SOPs) using advanced AI models for transcription, visual analysis, and content generation.

## 🏗️ Architecture

```
📁 Input Video (.mp4 / .mov / .webm)
  ↓
🎙️ Transcription — WhisperX
  ↓
🖼️ Frame Extraction — FFMPEG
  ↓
🧠 Visual Analysis — YOLOv8 + PaddleOCR
  ↓
🧩 Context Sync — Align audio + visuals via timestamps
  ↓
🧾 SOP Generation — LangChain + GPT-4o
  ↓
📄 Output — Structured SOP (numbered steps in .txt or .json)
```

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
2. **FFmpeg** - [Download FFmpeg](https://ffmpeg.org/download.html) and add to system PATH
3. **OpenAI API Key** - Get from [OpenAI Platform](https://platform.openai.com/api-keys)

### Installation

1. **Clone or download this project**
   ```bash
   git clone <repository-url>
   cd tasklane-ai-pipeline
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   # Copy template and edit
   copy env_template.txt .env
   
   # Edit .env file with your OpenAI API key
   OPENAI_API_KEY=sk-your-actual-api-key-here
   ```

5. **Check setup**
   ```bash
   python main.py --check-setup
   ```

## 📖 Usage

### Process a Single Video

```bash
python main.py --video "input_videos/demo.mp4"
```

### Process All Videos in Directory

```bash
python main.py
# or
python main.py --input-dir "input_videos" --output-dir "outputs"
```

### Command Line Options

```bash
python main.py --help
```

- `--video, -v`: Process a single video file
- `--input-dir, -i`: Input directory for videos (default: input_videos)
- `--output-dir, -o`: Output directory (default: outputs)
- `--check-setup`: Check if all dependencies are installed

## 📁 Project Structure

```
tasklane-ai-pipeline/
│
├── main.py                    # 🎯 Main pipeline orchestrator
├── requirements.txt           # 📦 Python dependencies
├── env_template.txt          # 🔧 Environment template
├── README.md                 # 📖 This file
│
├── transcription.py          # 🎙️ Audio transcription module
├── frame_extraction.py       # 🖼️ Frame extraction module
├── visual_analysis.py        # 🧠 Visual analysis module
├── sop_generation.py         # 🧾 SOP generation module
│
├── input_videos/             # 📹 Drop your videos here
│   ├── demo.mp4
│   └── tutorial.mov
│
└── outputs/                  # 📄 Generated outputs
    ├── transcripts/          # 🎙️ Audio transcripts
    ├── frames/               # 🖼️ Extracted frames
    ├── visual_data/          # 🧠 Visual analysis results
    └── sops/                 # 📋 Generated SOPs
```

## 🔧 Configuration

### Environment Variables (.env)

```bash
# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Model Configuration
WHISPER_MODEL=medium          # small, medium, large, large-v2
YOLO_MODEL=yolov8n.pt        # yolov8n.pt, yolov8s.pt, yolov8m.pt, yolov8l.pt, yolov8x.pt
DEVICE=cuda                   # cuda, cpu

# Processing Configuration
FRAME_EXTRACTION_FPS=1        # Frames per second to extract
```

### Model Options

- **WhisperX Models**: `small`, `medium`, `large`, `large-v2`
- **YOLO Models**: `yolov8n.pt` (nano), `yolov8s.pt` (small), `yolov8m.pt` (medium), `yolov8l.pt` (large), `yolov8x.pt` (xlarge)

## 📊 Output Format

### Generated SOP Example

```
1. Open the browser settings by clicking the gear icon.
2. Navigate to the "Privacy" section.
3. Click "Clear browsing data" and confirm.
4. Select the time range for data deletion.
5. Choose which data types to clear.
6. Click "Clear data" to complete the process.
```

### Output Files

- **`video_name_sop.txt`**: Plain text SOP
- **`video_name_sop.json`**: Structured JSON with steps
- **`video_name_summary.json`**: Processing metadata and statistics

## 🛠️ Technical Details

### AI Models Used

- **WhisperX**: Advanced speech recognition with word-level timestamps
- **YOLOv8**: Real-time object detection
- **PaddleOCR**: Text recognition and extraction
- **GPT-4o**: Natural language generation for SOP creation

### Processing Pipeline

1. **Audio Transcription**: Extract and timestamp spoken content
2. **Frame Extraction**: Sample video frames at configurable FPS
3. **Visual Analysis**: Detect objects and extract text from frames
4. **Context Alignment**: Match audio timestamps with visual elements
5. **SOP Generation**: Create structured procedures using AI

## 🎯 Use Cases

- **Training Videos**: Convert instructional content to SOPs
- **Process Documentation**: Automate procedure documentation
- **Quality Assurance**: Standardize operational procedures
- **Compliance**: Generate audit-ready documentation
- **Onboarding**: Create step-by-step guides for new employees

## 🔍 Troubleshooting

### Common Issues

1. **FFmpeg not found**
   - Install FFmpeg and add to system PATH
   - Windows: Download from https://ffmpeg.org/download.html

2. **CUDA/GPU issues**
   - Set `DEVICE=cpu` in .env for CPU-only processing
   - Install CUDA-compatible PyTorch version

3. **OpenAI API errors**
   - Verify API key in .env file
   - Check API quota and billing

4. **Memory issues**
   - Use smaller models (WhisperX small, YOLOv8n)
   - Reduce frame extraction FPS

### Performance Tips

- **GPU Processing**: Use CUDA for faster processing
- **Model Selection**: Choose appropriate model sizes for your needs
- **Frame Rate**: Lower FPS = fewer frames = faster processing
- **Batch Processing**: Process multiple videos in sequence

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **WhisperX**: Advanced speech recognition
- **Ultralytics**: YOLOv8 implementation
- **PaddleOCR**: Text recognition
- **OpenAI**: GPT-4o language model
- **FFmpeg**: Video processing

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the setup instructions
3. Open an issue on GitHub

---

**Made with ❤️ for automated content creation** 