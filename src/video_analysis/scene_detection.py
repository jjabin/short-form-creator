import cv2
import numpy as np
from scenedetect import detect, ContentDetector, AdaptiveDetector

class SceneDetector:
    def __init__(self, threshold=27.0, min_scene_len=15):
        self.threshold = threshold
        self.min_scene_len = min_scene_len
        self.content_detector = ContentDetector(threshold=self.threshold)
        self.adaptive_detector = AdaptiveDetector(min_scene_len=self.min_scene_len)
    
    def detect_scenes(self, video_path):
        """Detect scene changes in video"""
        scene_list = detect(video_path, [self.content_detector, self.adaptive_detector])
        
        scenes = []
        for scene in scene_list:
            scenes.append({
                'start': scene[0].get_seconds(),
                'end': scene[1].get_seconds(),
                'duration': scene[1].get_seconds() - scene[0].get_seconds()
            })
            
        return scenes
    
    def get_scene_transitions(self, scenes):
        """Get transition points between scenes"""
        transitions = []
        for i in range(len(scenes) - 1):
            transitions.append({
                'from_scene': scenes[i],
                'to_scene': scenes[i + 1],
                'timestamp': scenes[i]['end']
            })
        return transitions