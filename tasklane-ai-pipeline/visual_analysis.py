from ultralytics import YOLO
from paddleocr import PaddleOCR
import cv2
import os
import json
from dotenv import load_dotenv

load_dotenv()

class VisualAnalyzer:
    def __init__(self):
        """Initialize YOLO and PaddleOCR models"""
        print("🧠 Initializing visual analysis models...")
        
        # Load YOLO model
        model_name = os.getenv("YOLO_MODEL", "yolov8n.pt")
        self.yolo_model = YOLO(model_name)
        print(f"📦 Loaded YOLO model: {model_name}")
        
        # Load PaddleOCR
        self.ocr = PaddleOCR(use_angle_cls=True, lang='en', show_log=False)
        print("📝 Loaded PaddleOCR model")
        
        print("✅ Visual analysis models ready!")

    def analyze_frame(self, image_path):
        """
        Analyze a single frame for objects and text
        
        Args:
            image_path (str): Path to the image file
        
        Returns:
            dict: Analysis results containing YOLO and OCR data
        """
        if not os.path.exists(image_path):
            print(f"❌ Image not found: {image_path}")
            return None
        
        print(f"🔍 Analyzing frame: {os.path.basename(image_path)}")
        
        # YOLO object detection
        yolo_results = self.yolo_model(image_path, verbose=False)
        
        # Extract YOLO detections
        yolo_data = []
        for result in yolo_results:
            if result.boxes is not None:
                for box in result.boxes:
                    detection = {
                        'class': int(box.cls[0]),
                        'class_name': result.names[int(box.cls[0])],
                        'confidence': float(box.conf[0]),
                        'bbox': box.xyxy[0].tolist()  # [x1, y1, x2, y2]
                    }
                    yolo_data.append(detection)
        
        # PaddleOCR text detection
        ocr_results = self.ocr.ocr(image_path, cls=True)
        
        # Extract OCR data
        ocr_data = []
        if ocr_results and ocr_results[0]:
            for line in ocr_results[0]:
                if line:
                    text_info = {
                        'text': line[1][0],  # Detected text
                        'confidence': line[1][1],  # Confidence score
                        'bbox': line[0]  # Bounding box coordinates
                    }
                    ocr_data.append(text_info)
        
        return {
            'frame': os.path.basename(image_path),
            'yolo_detections': yolo_data,
            'ocr_text': ocr_data,
            'objects_count': len(yolo_data),
            'text_count': len(ocr_data)
        }

    def analyze_frames_batch(self, frame_paths, output_dir):
        """
        Analyze multiple frames and save results
        
        Args:
            frame_paths (list): List of frame file paths
            output_dir (str): Directory to save analysis results
        
        Returns:
            list: List of analysis results for each frame
        """
        print(f"🔄 Starting batch analysis of {len(frame_paths)} frames...")
        
        os.makedirs(output_dir, exist_ok=True)
        results = []
        
        for i, frame_path in enumerate(frame_paths):
            print(f"📊 Processing frame {i+1}/{len(frame_paths)}: {os.path.basename(frame_path)}")
            
            result = self.analyze_frame(frame_path)
            if result:
                results.append(result)
                
                # Save individual frame result
                frame_name = os.path.splitext(os.path.basename(frame_path))[0]
                result_path = os.path.join(output_dir, f"{frame_name}_analysis.json")
                with open(result_path, 'w') as f:
                    json.dump(result, f, indent=2)
        
        # Save combined results
        combined_path = os.path.join(output_dir, "combined_analysis.json")
        with open(combined_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"✅ Analysis complete! Results saved to: {output_dir}")
        return results

    def get_summary(self, analysis_results):
        """
        Generate a summary of visual analysis results
        
        Args:
            analysis_results (list): List of frame analysis results
        
        Returns:
            dict: Summary statistics
        """
        total_objects = sum(r['objects_count'] for r in analysis_results)
        total_text = sum(r['text_count'] for r in analysis_results)
        
        # Get unique object classes
        object_classes = set()
        for result in analysis_results:
            for detection in result['yolo_detections']:
                object_classes.add(detection['class_name'])
        
        # Get all detected text
        all_text = []
        for result in analysis_results:
            for text_info in result['ocr_text']:
                all_text.append(text_info['text'])
        
        return {
            'total_frames': len(analysis_results),
            'total_objects_detected': total_objects,
            'total_text_detected': total_text,
            'unique_object_classes': list(object_classes),
            'detected_text': all_text,
            'average_objects_per_frame': total_objects / len(analysis_results) if analysis_results else 0,
            'average_text_per_frame': total_text / len(analysis_results) if analysis_results else 0
        } 