from dotenv import load_dotenv
import os
import json
import time
import asyncio
import aiofiles
from concurrent.futures import ThreadPoolExecutor
import multiprocessing as mp
from typing import List, Dict, Any, Optional
import cv2
import numpy as np
from functools import lru_cache
import pickle
import hashlib
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Global model cache with persistence
MODEL_CACHE_DIR = "cache/models"
CACHE_DIR = "cache"
os.makedirs(MODEL_CACHE_DIR, exist_ok=True)
os.makedirs(CACHE_DIR, exist_ok=True)

class ModelCache:
    """Persistent model cache with automatic loading/saving"""
    
    def __init__(self):
        self._models = {}
        self._model_paths = {
            'whisper': os.path.join(MODEL_CACHE_DIR, 'whisper_model.pkl'),
            'yolo': os.path.join(MODEL_CACHE_DIR, 'yolo_model.pkl'),
        }
    
    def get_model(self, model_type: str):
        """Get cached model or load if not cached"""
        if model_type not in self._models:
            self._models[model_type] = self._load_model(model_type)
        return self._models[model_type]
    
    def _load_model(self, model_type: str):
        """Load model from cache or create new"""
        cache_path = self._model_paths[model_type]
        
        if os.path.exists(cache_path):
            logger.info(f"Loading {model_type} model from cache...")
            try:
                with open(cache_path, 'rb') as f:
                    return pickle.load(f)
            except Exception as e:
                logger.warning(f"Failed to load cached {model_type} model: {e}")
        
        logger.info(f"Loading fresh {model_type} model...")
        model = self._create_model(model_type)
        
        # Cache the model
        try:
            with open(cache_path, 'wb') as f:
                pickle.dump(model, f)
        except Exception as e:
            logger.warning(f"Failed to cache {model_type} model: {e}")
        
        return model
    
    def _create_model(self, model_type: str):
        """Create a new model instance"""
        if model_type == 'whisper':
            import whisper
            return whisper.load_model("medium")
        elif model_type == 'yolo':
            from ultralytics import YOLO
            return YOLO("yolov8n.pt")
        else:
            raise ValueError(f"Unknown model type: {model_type}")

# Global model cache instance
model_cache = ModelCache()

class VideoProcessor:
    """Scalable video processing with full frame analysis"""
    
    def __init__(self, video_path: str, output_dir: str):
        self.video_path = video_path
        self.output_dir = output_dir
        self.cache_key = self._generate_cache_key()
        
        # Create output directories
        for subdir in ['transcripts', 'frames', 'visual_data', 'sops']:
            os.makedirs(os.path.join(output_dir, subdir), exist_ok=True)
    
    def _generate_cache_key(self) -> str:
        """Generate cache key based on video file"""
        file_hash = hashlib.md5(open(self.video_path, 'rb').read()).hexdigest()
        return f"{Path(self.video_path).stem}_{file_hash[:8]}"
    
    async def process_video_async(self):
        """Process video asynchronously with full functionality"""
        start_time = time.time()
        
        logger.info("🚀 Starting scalable video processing pipeline...")
        
        # Step 1: Load all models in parallel
        logger.info("[1/5] Loading models in parallel...")
        models = await self._load_models_async()
        
        # Step 2: Transcribe video
        logger.info("[2/5] Transcribing video...")
        transcript = await self._transcribe_video_async(models['whisper'])
        
        # Step 3: Extract ALL frames (maintain full functionality)
        logger.info("[3/5] Extracting all frames...")
        frame_paths = await self._extract_all_frames_async()
        
        # Step 4: Analyze frames with threading (avoid pickling issues)
        logger.info("[4/5] Analyzing frames with threaded processing...")
        visual_output = await self._analyze_frames_threaded_async(frame_paths, models['yolo'])
        
        # Step 5: Generate comprehensive SOP
        logger.info("[5/5] Generating comprehensive SOP...")
        sop_text = await self._generate_sop_async(transcript, visual_output)
        
        # Save results
        output_path = os.path.join(self.output_dir, "sops", f"{self.cache_key}_sop.txt")
        async with aiofiles.open(output_path, 'w', encoding='utf-8') as f:
            await f.write(sop_text)
        
        total_time = time.time() - start_time
        logger.info(f"🎉 Pipeline completed in {total_time:.2f}s")
        logger.info(f"📄 SOP saved to {output_path}")
        
        return {
            'transcript': transcript,
            'visual_output': visual_output,
            'sop': sop_text,
            'processing_time': total_time,
            'frames_processed': len(frame_paths)
        }
    
    async def _load_models_async(self) -> Dict[str, Any]:
        """Load all models asynchronously"""
        loop = asyncio.get_event_loop()
        
        # Load models in parallel using thread pool
        with ThreadPoolExecutor(max_workers=2) as executor:
            whisper_future = loop.run_in_executor(
                executor, model_cache.get_model, 'whisper'
            )
            yolo_future = loop.run_in_executor(
                executor, model_cache.get_model, 'yolo'
            )
            
            models = await asyncio.gather(whisper_future, yolo_future)
        
        return {
            'whisper': models[0],
            'yolo': models[1]
        }
    
    async def _transcribe_video_async(self, whisper_model) -> Dict:
        """Transcribe video asynchronously"""
        loop = asyncio.get_event_loop()
        
        def transcribe():
            return whisper_model.transcribe(self.video_path)
        
        result = await loop.run_in_executor(None, transcribe)
        
        # Save transcript
        output_path = os.path.join(self.output_dir, "transcripts", f"{self.cache_key}_transcript.json")
        async with aiofiles.open(output_path, 'w', encoding='utf-8') as f:
            await f.write(json.dumps(result, ensure_ascii=False, indent=4))
        
        return result
    
    async def _extract_all_frames_async(self) -> List[str]:
        """Extract ALL frames from video (maintain full functionality)"""
        loop = asyncio.get_event_loop()
        
        def extract_frames():
            import ffmpeg
            
            output_pattern = os.path.join(self.output_dir, "frames", f"{self.cache_key}_frame_%04d.png")
            
            # Extract frames at 1 FPS (maintain original functionality)
            (
                ffmpeg
                .input(self.video_path)
                .filter('fps', fps=1)
                .output(output_pattern)
                .run(overwrite_output=True, quiet=True)
            )
            
            # Get all extracted frame paths
            frame_dir = os.path.join(self.output_dir, "frames")
            frame_files = sorted([f for f in os.listdir(frame_dir) if f.startswith(f"{self.cache_key}_")])
            return [os.path.join(frame_dir, f) for f in frame_files]
        
        return await loop.run_in_executor(None, extract_frames)
    
    async def _analyze_frames_threaded_async(self, frame_paths: List[str], yolo_model) -> List[Dict]:
        """Analyze frames using threaded processing (avoid pickling issues)"""
        loop = asyncio.get_event_loop()
        
        # Process frames in batches for better resource utilization
        batch_size = min(10, len(frame_paths))  # Process 10 frames at a time
        visual_output = []
        
        for i in range(0, len(frame_paths), batch_size):
            batch = frame_paths[i:i + batch_size]
            logger.info(f"Processing batch {i//batch_size + 1}/{(len(frame_paths) + batch_size - 1)//batch_size}")
            
            # Process batch with threading (avoid multiprocessing pickling issues)
            with ThreadPoolExecutor(max_workers=min(4, len(batch))) as executor:
                batch_results = await asyncio.gather(*[
                    loop.run_in_executor(executor, self._analyze_single_frame, frame_path, yolo_model)
                    for frame_path in batch
                ])
            
            visual_output.extend([r for r in batch_results if r is not None])
        
        return visual_output
    
    def _analyze_single_frame(self, frame_path: str, yolo_model) -> Optional[Dict]:
        """Analyze a single frame (for threading)"""
        try:
            # YOLO analysis
            yolo_results = yolo_model(frame_path, verbose=False)
            
            yolo_data = []
            for result in yolo_results:
                if result.boxes is not None:
                    for box in result.boxes:
                        yolo_data.append({
                            "class": yolo_model.names[int(box.cls)],
                            "confidence": float(box.conf),
                            "bbox": box.xyxy.tolist(),
                        })
            
            # OCR analysis (simplified to avoid pickling issues)
            try:
                from paddleocr import PaddleOCR
                ocr = PaddleOCR(use_textline_orientation=True, lang='en')
                ocr_output = ocr.ocr(frame_path, cls=False)
                ocr_data = []
                if ocr_output:
                    for block in ocr_output:
                        for line in block:
                            if len(line) > 1:
                                text = line[1][0]
                                if len(text.strip()) > 2:  # Filter noise
                                    ocr_data.append(text)
            except Exception as e:
                logger.warning(f"OCR analysis failed for {frame_path}: {e}")
                ocr_data = []
            
            return {
                "frame": os.path.basename(frame_path),
                "yolo": yolo_data,
                "ocr": ocr_data,
            }
        except Exception as e:
            logger.error(f"Error processing frame {frame_path}: {e}")
            return None
    
    async def _generate_sop_async(self, transcript: Dict, visual_output: List[Dict]) -> str:
        """Generate comprehensive SOP asynchronously"""
        loop = asyncio.get_event_loop()
        
        def generate_sop():
            from openai import OpenAI
            import os
            
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            
            # Create comprehensive prompt with full data
            prompt = f"""
You are an expert technical writer specializing in creating detailed, comprehensive Standard Operating Procedures (SOPs).

Given the following complete video transcript and visual analysis data, create a thorough, step-by-step SOP that captures all important details.

TRANSCRIPT:
{json.dumps(transcript, indent=2)}

VISUAL ANALYSIS (All Frames):
{json.dumps(visual_output, indent=2)}

Instructions:
1. Create a comprehensive SOP that captures ALL important steps
2. Use the visual data to identify UI elements, buttons, text, and objects
3. Include specific details about what users should see and interact with
4. Number each step clearly (1, 2, 3, etc.)
5. Be thorough but well-organized
6. Include any error states or important UI elements detected

Format your response as a detailed, numbered SOP:
"""
            
            response = client.chat.completions.create(
                model="gpt-4o",  # Use full GPT-4 for comprehensive analysis
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2000,  # Allow for comprehensive SOP
                temperature=0.2,  # Consistent output
            )
            
            return response.choices[0].message.content
        
        return await loop.run_in_executor(None, generate_sop)

async def main_scalable_simple():
    """Main scalable processing function"""
    video_path = "input_videos/demo.mp4"
    output_dir = "outputs"
    
    if not os.path.exists(video_path):
        logger.error(f"Video file not found: {video_path}")
        return
    
    processor = VideoProcessor(video_path, output_dir)
    results = await processor.process_video_async()
    
    # Print performance summary
    logger.info(f"\n📊 Performance Summary:")
    logger.info(f"   • Total time: {results['processing_time']:.2f}s")
    logger.info(f"   • Frames processed: {results['frames_processed']}")
    logger.info(f"   • Objects detected: {sum(len(frame.get('yolo', [])) for frame in results['visual_output'])}")
    logger.info(f"   • Text blocks detected: {sum(len(frame.get('ocr', [])) for frame in results['visual_output'])}")

if __name__ == "__main__":
    asyncio.run(main_scalable_simple()) 