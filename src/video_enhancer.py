import cv2
import numpy as np
from typing import Tuple

class VideoEnhancer:
    def __init__(self):
        pass

    def enhance_frame(self, frame: np.ndarray) -> np.ndarray:
        """Apply various enhancements to a video frame."""
        # Convert to float32 for processing
        frame_float = frame.astype(np.float32) / 255.0

        # Apply enhancements
        frame_enhanced = self._adjust_brightness_contrast(frame_float)
        frame_enhanced = self._enhance_sharpness(frame_enhanced)
        frame_enhanced = self._enhance_colors(frame_enhanced)

        # Convert back to uint8
        return (frame_enhanced * 255).clip(0, 255).astype(np.uint8)

    def _adjust_brightness_contrast(self, 
                                  frame: np.ndarray,
                                  brightness: float = 1.0,
                                  contrast: float = 1.2) -> np.ndarray:
        """Adjust brightness and contrast of the frame."""
        return np.clip(contrast * (frame - 0.5) + 0.5 + brightness - 1, 0, 1)

    def _enhance_sharpness(self, 
                          frame: np.ndarray,
                          amount: float = 1.5) -> np.ndarray:
        """Enhance frame sharpness using unsharp masking."""
        # Create blurred version
        blurred = cv2.GaussianBlur(frame, (0, 0), 3)
        # Apply unsharp mask
        return np.clip(frame + (frame - blurred) * (amount - 1), 0, 1)

    def _enhance_colors(self, 
                       frame: np.ndarray,
                       saturation: float = 1.2) -> np.ndarray:
        """Enhance colors in the frame."""
        # Convert to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
        # Adjust saturation
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * saturation, 0, 1)
        # Convert back to RGB
        return cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)

    def add_cinematic_bars(self, 
                          frame: np.ndarray,
                          ratio: float = 2.35) -> np.ndarray:
        """Add cinematic black bars to frame."""
        height, width = frame.shape[:2]
        target_height = int(width / ratio)
        
        if target_height >= height:
            return frame
        
        bar_height = (height - target_height) // 2
        result = np.zeros_like(frame)
        result[bar_height:height-bar_height, :] = frame[bar_height:height-bar_height, :]
        
        return result

    def apply_vignette(self, 
                      frame: np.ndarray,
                      strength: float = 0.3) -> np.ndarray:
        """Apply vignette effect to frame."""
        height, width = frame.shape[:2]
        
        # Create radial gradient
        x = np.linspace(-1, 1, width)
        y = np.linspace(-1, 1, height)
        X, Y = np.meshgrid(x, y)
        radius = np.sqrt(X**2 + Y**2)
        
        # Create vignette mask
        mask = 1 - np.clip(radius * strength, 0, 1)
        mask = np.dstack([mask] * 3)
        
        # Apply vignette
        return (frame * mask).astype(np.uint8)
