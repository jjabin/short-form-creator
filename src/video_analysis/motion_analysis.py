import cv2
import numpy as np

class MotionAnalyzer:
    def __init__(self):
        self.history = 20
        self.thresh = 32
        self.detect_shadows = False
        self.background_subtractor = cv2.createBackgroundSubtractorMOG2(
            history=self.history,
            varThreshold=self.thresh,
            detectShadows=self.detect_shadows
        )
    
    def analyze_motion(self, frame):
        """Analyze motion in a single frame"""
        fg_mask = self.background_subtractor.apply(frame)
        contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        motion_areas = []
        for contour in contours:
            if cv2.contourArea(contour) > 100:  # Filter small movements
                x, y, w, h = cv2.boundingRect(contour)
                motion_areas.append((x, y, w, h))
                
        return motion_areas
    
    def get_dynamic_crop(self, frame, motion_areas):
        """Calculate optimal crop based on motion"""
        if not motion_areas:
            return None
            
        # Combine all motion areas
        x_coords = [x for x, _, _, _ in motion_areas]
        y_coords = [y for _, y, _, _ in motion_areas]
        w_coords = [w for _, _, w, _ in motion_areas]
        h_coords = [h for _, _, _, h in motion_areas]
        
        # Calculate crop dimensions
        crop_x = min(x_coords)
        crop_y = min(y_coords)
        crop_w = max([x + w for x, _, w, _ in motion_areas]) - crop_x
        crop_h = max([y + h for _, y, _, h in motion_areas]) - crop_y
        
        return crop_x, crop_y, crop_w, crop_h