import ffmpeg
import os
from dotenv import load_dotenv

load_dotenv()

def extract_frames(video_path, output_dir, fps=None):
    """
    Extract frames from video using FFmpeg
    
    Args:
        video_path (str): Path to the input video file
        output_dir (str): Directory to save extracted frames
        fps (int, optional): Frames per second to extract. Defaults to env var or 1.
    
    Returns:
        list: List of extracted frame file paths
    """
    print(f"🔄 Starting frame extraction for: {video_path}")
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Get FPS from environment or use default
    if fps is None:
        fps = int(os.getenv("FRAME_EXTRACTION_FPS", "1"))
    
    print(f"📸 Extracting frames at {fps} FPS...")
    
    # Get video info
    try:
        probe = ffmpeg.probe(video_path)
        video_info = next(s for s in probe['streams'] if s['codec_type'] == 'video')
        duration = float(probe['format']['duration'])
        print(f"📹 Video duration: {duration:.2f} seconds")
    except Exception as e:
        print(f"⚠️ Warning: Could not probe video info: {e}")
    
    # Extract frames
    output_pattern = os.path.join(output_dir, 'frame_%04d.png')
    
    try:
        (
            ffmpeg
            .input(video_path)
            .filter('fps', fps=fps)
            .output(output_pattern, vcodec='png')
            .run(overwrite_output=True, quiet=True)
        )
        
        # Get list of extracted frames
        frame_files = [f for f in os.listdir(output_dir) if f.startswith('frame_') and f.endswith('.png')]
        frame_files.sort()
        
        print(f"✅ Extracted {len(frame_files)} frames to: {output_dir}")
        
        return [os.path.join(output_dir, f) for f in frame_files]
        
    except ffmpeg.Error as e:
        print(f"❌ Error extracting frames: {e}")
        return []

def get_frame_timestamp(frame_filename, fps=None):
    """
    Calculate timestamp for a frame based on filename
    
    Args:
        frame_filename (str): Frame filename (e.g., 'frame_0001.png')
        fps (int, optional): Frames per second. Defaults to env var or 1.
    
    Returns:
        float: Timestamp in seconds
    """
    if fps is None:
        fps = int(os.getenv("FRAME_EXTRACTION_FPS", "1"))
    
    # Extract frame number from filename
    try:
        frame_num = int(frame_filename.split('_')[1].split('.')[0])
        return frame_num / fps
    except (IndexError, ValueError):
        return 0.0 