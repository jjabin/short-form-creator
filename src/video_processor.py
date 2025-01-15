import cv2
import numpy as np
from moviepy.editor import VideoFileClip
from scenedetect import detect, ContentDetector
from typing import List, Tuple

class VideoProcessor:
    def __init__(self, video_path: str):
        self.video_path = video_path
        self.clip = VideoFileClip(video_path)
        
    def detect_scenes(self) -> List[Tuple[float, float]]:
        """Detect scene changes in the video."""
        scenes = detect(self.video_path, ContentDetector())
        return [(scene[0].get_seconds(), scene[1].get_seconds()) for scene in scenes]
    
    def extract_clip(self, start_time: float, end_time: float, output_path: str):
        """Extract a clip from the video between start_time and end_time."""
        subclip = self.clip.subclip(start_time, end_time)
        subclip.write_videofile(output_path, codec='libx264')
        
    def smart_crop_vertical(self, frame: np.ndarray) -> np.ndarray:
        """Intelligently crop a frame to vertical format (9:16 ratio)."""
        height, width = frame.shape[:2]
        target_width = int(height * 9/16)
        
        # Detect faces or important objects to center the crop
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        if len(faces) > 0:
            # Center crop around the largest face
            face_x = faces[0][0] + faces[0][2]//2
            crop_x = max(0, min(width - target_width, face_x - target_width//2))
        else:
            # Default to center crop if no faces detected
            crop_x = (width - target_width) // 2
            
        return frame[:, crop_x:crop_x+target_width]
    
    def process_clip_vertical(self, start_time: float, end_time: float, output_path: str):
        """Process a clip and convert it to vertical format."""
        subclip = self.clip.subclip(start_time, end_time)
        frames = [self.smart_crop_vertical(frame) for frame in subclip.iter_frames()]
        
        # Create new clip from processed frames
        new_clip = VideoFileClip(output_path, audio=subclip.audio)
        new_clip.write_videofile(output_path)
        
    def cleanup(self):
        """Release resources."""
        self.clip.close()