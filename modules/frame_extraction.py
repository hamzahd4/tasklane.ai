import ffmpeg
import os
 
def extract_frames(video_path, output_dir, fps=1):
    os.makedirs(output_dir, exist_ok=True)
    (
        ffmpeg
        .input(video_path)
        .filter('fps', fps=fps)
        .output(os.path.join(output_dir, 'frame_%04d.png'))
        .run(overwrite_output=True)
    )