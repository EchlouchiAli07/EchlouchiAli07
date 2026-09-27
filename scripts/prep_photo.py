import os
import sys
import cv2
import numpy as np
from PIL import Image

def prep_photo(input_path, output_path):
    print(f"Loading {input_path}...")
    img = cv2.imread(input_path)
    if img is None:
        raise ValueError(f"Could not load image at {input_path}")
        
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply CLAHE for high contrast details (eyes, hair, features)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    enhanced = clahe.apply(gray)
    
    # Normalize brightness & stretch contrast
    # Map background (which is light gray in photo) to pure white (255)
    # So spaces ' ' are rendered in ASCII
    normalized = cv2.normalize(enhanced, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
    
    # Light background boost
    # Anything above 210 gets pushed towards 255 (white)
    mask = normalized > 200
    normalized[mask] = np.clip(normalized[mask] * 1.15, 0, 255).astype(np.uint8)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    cv2.imwrite(output_path, normalized)
    print(f"Prepped image saved to {output_path}")

if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else os.path.join("photo", "portrait-professionnel (1).png")
    dst = os.path.join("data", "source-prepped.png")
    prep_photo(src, dst)
