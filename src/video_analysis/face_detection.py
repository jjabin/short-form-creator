import cv2
import numpy as np
from mtcnn import MTCNN

class FaceDetector:
    def __init__(self):
        self.detector = MTCNN()
        
    def detect_faces(self, frame):
        """Detect faces in a single frame"""
        results = self.detector.detect_faces(frame)
        return [(face['box'], face['confidence']) for face in results]
    
    def track_faces(self, video_path):
        """Track faces across video frames"""
        cap = cv2.VideoCapture(video_path)
        face_tracks = []
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
                
            faces = self.detect_faces(frame)
            face_tracks.append(faces)
            
        cap.release()
        return face_tracks