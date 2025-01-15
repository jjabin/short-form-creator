import cv2
import numpy as np
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, TextClip
from typing import List, Tuple, Optional

class ClipGenerator:
    def __init__(self, input_path: str):
        self.input_path = input_path
        self.clip = VideoFileClip(input_path)
    
    def create_short(self,
                     start_time: float,
                     end_time: float,
                     output_path: str,
                     captions: Optional[List[Dict]] = None,
                     background_music: Optional[str] = None):
        """Create a short-form clip with captions and background music."""
        # Extract subclip
        subclip = self.clip.subclip(start_time, end_time)
        
        # Convert to vertical format if needed
        if subclip.w > subclip.h:
            subclip = self._convert_to_vertical(subclip)
        
        # Add captions if provided
        if captions:
            subclip = self._add_captions(subclip, captions)
        
        # Add background music if provided
        if background_music:
            subclip = self._add_background_music(subclip, background_music)
        
        # Write output
        subclip.write_videofile(output_path)
    
    def _convert_to_vertical(self, clip) -> VideoFileClip:
        """Convert horizontal video to vertical format."""
        target_ratio = 9/16
        current_ratio = clip.w / clip.h
        
        if current_ratio > target_ratio:
            # Crop width to match target ratio
            new_width = int(clip.h * target_ratio)
            x_center = clip.w // 2
            x1 = x_center - (new_width // 2)
            x2 = x_center + (new_width // 2)
            return clip.crop(x1=x1, x2=x2)
        
        return clip
    
    def _add_captions(self, clip: VideoFileClip, captions: List[Dict]) -> CompositeVideoClip:
        """Add captions to the video clip."""
        text_clips = []
        
        for caption in captions:
            text_clip = TextClip(
                caption['text'],
                fontsize=40,
                color='white',
                stroke_color='black',
                stroke_width=2
            ).set_position(('center', 'bottom'))
            
            text_clip = text_clip.set_start(caption['start']).set_end(caption['end'])
            text_clips.append(text_clip)
        
        return CompositeVideoClip([clip] + text_clips)
    
    def _add_background_music(self,
                             clip: VideoFileClip,
                             music_path: str,
                             volume: float = 0.3) -> VideoFileClip:
        """Add background music to the video clip."""
        background_music = AudioFileClip(music_path)
        
        # Loop music if needed
        if background_music.duration < clip.duration:
            n_loops = int(np.ceil(clip.duration / background_music.duration))
            background_music = background_music.loop(n=n_loops)
        
        # Trim to clip duration
        background_music = background_music.subclip(0, clip.duration)
        
        # Set volume
        background_music = background_music.volumex(volume)
        
        # Composite audio
        clip = clip.set_audio(
            CompositeVideoClip([clip]).audio.audio_fadein(1).audio_fadeout(1)
        )
        
        return clip
    
    def close(self):
        """Release resources."""
        self.clip.close()