import cv2
import numpy as np
from scenedetect import detect, ContentDetector
from typing import List, Tuple

class VideoProcessor:
    def __init__(self, input_path: str):
        self.input_path = input_path
        self.cap = cv2.VideoCapture(input_path)
        
    def detect_scenes(self) -> List[Tuple[float, float]]:
        """Detect scene changes in the video."""
        scenes = detect(self.input_path, ContentDetector())
        return [(scene[0].get_seconds(), scene[1].get_seconds()) for scene in scenes]
    
    def extract_clip(self, start_time: float, end_time: float, output_path: str):
        """Extract a clip from the video between start_time and end_time."""
        import subprocess
        
        command = [
            'ffmpeg', '-i', self.input_path,
            '-ss', str(start_time),
            '-t', str(end_time - start_time),
            '-c:v', 'libx264', '-c:a', 'aac',
            output_path
        ]
        
        subprocess.run(command, check=True)
    
    def get_frame(self, timestamp: float) -> np.ndarray:
        """Get a frame at the specified timestamp."""
        self.cap.set(cv2.CAP_PROP_POS_MSEC, timestamp * 1000)
        ret, frame = self.cap.read()
        if ret:
            return frame
        raise ValueError(f'Could not read frame at timestamp {timestamp}')
    
    def close(self):
        """Release video capture resources."""
        self.cap.release()