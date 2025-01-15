import cv2
import numpy as np
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, TextClip
from typing import List, Dict, Tuple, Optional

class ClipComposer:
    """Advanced video composition and editing engine."""
    
    def __init__(self, video_path: str):
        self.video = VideoFileClip(video_path)
    
    def create_short_form(self,
                         segments: List[Dict],
                         style: Dict,
                         captions: Optional[List[Dict]] = None,
                         music_path: Optional[str] = None) -> VideoFileClip:
        """Create platform-optimized short-form content."""
        clips = []
        
        for segment in segments:
            # Extract and process segment
            clip = self.video.subclip(segment['start'], segment['end'])
            
            # Apply visual enhancements
            if style.get('vertical', False):
                clip = self._convert_to_vertical(clip)
            if style.get('zoom', 1.0) != 1.0:
                clip = self._apply_zoom(clip, style['zoom'])
            
            clips.append(clip)
        
        # Compose final video
        final_clip = CompositeVideoClip(clips)
        
        # Add captions if provided
        if captions:
            final_clip = self._add_captions(final_clip, captions)
        
        # Add music if provided
        if music_path:
            final_clip = self._add_background_music(final_clip, music_path)
        
        return final_clip
    
    def _convert_to_vertical(self, clip: VideoFileClip) -> VideoFileClip:
        """Convert to vertical format with smart cropping."""
        target_ratio = 9/16
        
        def get_smart_crop(frame):
            # Implement face/object detection for smart cropping
            # For now, use center crop
            h, w = frame.shape[:2]
            new_w = int(h * target_ratio)
            start = (w - new_w) // 2
            return frame[:, start:start+new_w]
        
        return clip.fl_image(get_smart_crop)
    
    def _apply_zoom(self, clip: VideoFileClip, zoom_factor: float) -> VideoFileClip:
        """Apply smooth zoom effect."""
        def zoom(frame):
            h, w = frame.shape[:2]
            M = cv2.getRotationMatrix2D((w/2, h/2), 0, zoom_factor)
            return cv2.warpAffine(frame, M, (w, h))
        
        return clip.fl_image(zoom)
    
    def _add_captions(self, clip: VideoFileClip, captions: List[Dict]) -> CompositeVideoClip:
        """Add dynamic captions with modern styling."""
        text_clips = []
        
        for caption in captions:
            text_clip = TextClip(
                caption['text'],
                fontsize=caption.get('fontsize', 40),
                color=caption.get('color', 'white'),
                font=caption.get('font', 'Arial-Bold'),
                stroke_color=caption.get('stroke_color', 'black'),
                stroke_width=caption.get('stroke_width', 2)
            ).set_position(caption.get('position', ('center', 'bottom')))
            
            text_clip = text_clip.set_start(caption['start']).set_end(caption['end'])
            
            if caption.get('animate', False):
                text_clip = text_clip.crossfadein(0.5)
            
            text_clips.append(text_clip)
        
        return CompositeVideoClip([clip] + text_clips)