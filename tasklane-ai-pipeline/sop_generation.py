from openai import OpenAI
import os
import json
from dotenv import load_dotenv

load_dotenv()

class SOPGenerator:
    def __init__(self):
        """Initialize OpenAI client for SOP generation"""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        self.client = OpenAI(api_key=api_key)
        print("🤖 SOP Generator initialized with OpenAI")

    def generate_sop(self, transcript_data, visual_data, video_name="video"):
        """
        Generate SOP from transcript and visual analysis data
        
        Args:
            transcript_data (dict): WhisperX transcription result
            visual_data (list): Visual analysis results from frames
            video_name (str): Name of the video for output file
        
        Returns:
            str: Generated SOP text
        """
        print("🧾 Generating SOP from transcript and visual data...")
        
        # Extract transcript text
        transcript_text = self._extract_transcript_text(transcript_data)
        
        # Extract visual summary
        visual_summary = self._extract_visual_summary(visual_data)
        
        # Create prompt for SOP generation
        prompt = self._create_sop_prompt(transcript_text, visual_summary)
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert technical writer specializing in creating clear, step-by-step Standard Operating Procedures (SOPs). You excel at converting video content into structured, actionable instructions."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=2000
            )
            
            sop_text = response.choices[0].message.content
            print("✅ SOP generated successfully!")
            
            return sop_text
            
        except Exception as e:
            print(f"❌ Error generating SOP: {e}")
            return None

    def _extract_transcript_text(self, transcript_data):
        """Extract plain text from transcript data"""
        if isinstance(transcript_data, dict):
            if "segments" in transcript_data:
                return " ".join([segment["text"] for segment in transcript_data["segments"]])
            return transcript_data.get("text", "")
        return str(transcript_data)

    def _extract_visual_summary(self, visual_data):
        """Extract meaningful visual information"""
        if not visual_data:
            return "No visual data available"
        
        summary = []
        
        # Group by objects and text
        all_objects = []
        all_text = []
        
        for frame_data in visual_data:
            if isinstance(frame_data, dict):
                # Extract objects
                for detection in frame_data.get('yolo_detections', []):
                    all_objects.append(detection.get('class_name', ''))
                
                # Extract text
                for text_info in frame_data.get('ocr_text', []):
                    all_text.append(text_info.get('text', ''))
        
        # Create summary
        if all_objects:
            object_counts = {}
            for obj in all_objects:
                object_counts[obj] = object_counts.get(obj, 0) + 1
            
            summary.append("Objects detected: " + ", ".join([f"{obj} ({count})" for obj, count in object_counts.items()]))
        
        if all_text:
            summary.append("Text detected: " + ", ".join(all_text))
        
        return "; ".join(summary) if summary else "No significant visual elements detected"

    def _create_sop_prompt(self, transcript_text, visual_summary):
        """Create the prompt for SOP generation"""
        return f"""
You are an expert technical writer creating a Standard Operating Procedure (SOP) from video content.

VIDEO TRANSCRIPT:
{transcript_text}

VISUAL ANALYSIS:
{visual_summary}

TASK: Create a clear, numbered step-by-step SOP based on the video content. Consider both the audio narration and visual elements.

REQUIREMENTS:
1. Use numbered steps (1, 2, 3, etc.)
2. Be specific and actionable
3. Include relevant visual cues when mentioned
4. Use clear, professional language
5. Keep steps concise but complete
6. Focus on the main workflow/task being demonstrated

FORMAT:
1. [First step description]
2. [Second step description]
3. [Continue with numbered steps...]

Generate the SOP now:
"""

    def save_sop(self, sop_text, output_dir, video_name="video"):
        """
        Save SOP to file
        
        Args:
            sop_text (str): Generated SOP text
            output_dir (str): Directory to save SOP
            video_name (str): Name of the video
        
        Returns:
            str: Path to saved SOP file
        """
        os.makedirs(output_dir, exist_ok=True)
        
        # Clean video name for filename
        safe_name = "".join(c for c in video_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_name = safe_name.replace(' ', '_')
        
        # Save as text file
        txt_path = os.path.join(output_dir, f"{safe_name}_sop.txt")
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(sop_text)
        
        # Save as JSON for structured data
        json_path = os.path.join(output_dir, f"{safe_name}_sop.json")
        sop_data = {
            "video_name": video_name,
            "sop_text": sop_text,
            "steps": self._extract_steps(sop_text)
        }
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(sop_data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 SOP saved to: {txt_path}")
        print(f"💾 Structured SOP saved to: {json_path}")
        
        return txt_path

    def _extract_steps(self, sop_text):
        """Extract individual steps from SOP text"""
        steps = []
        lines = sop_text.split('\n')
        
        for line in lines:
            line = line.strip()
            if line and line[0].isdigit() and '.' in line:
                # Extract step number and description
                parts = line.split('.', 1)
                if len(parts) == 2:
                    step_num = parts[0].strip()
                    step_desc = parts[1].strip()
                    steps.append({
                        "step_number": int(step_num),
                        "description": step_desc
                    })
        
        return steps 