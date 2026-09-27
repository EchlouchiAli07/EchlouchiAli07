import cv2
import numpy as np
import os

def process_portrait(input_path, output_path, width=80):
    img = cv2.imread(input_path)
    if img is None:
        raise ValueError(f"Could not load {input_path}")
        
    h, w, _ = img.shape
    
    # 1. Crop to focus on face and upper chest for max detail
    # The image is 1080x1200 approx. Crop top 5% to 85%
    crop_top = int(h * 0.05)
    crop_bottom = int(h * 0.85)
    crop_left = int(w * 0.10)
    crop_right = int(w * 0.90)
    
    cropped = img[crop_top:crop_bottom, crop_left:crop_right]
    
    # 2. Convert to grayscale
    gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
    
    # 3. Bilateral filter to smooth skin noise while preserving sharp edges (glasses, beard, eyes)
    filtered = cv2.bilateralFilter(gray, d=9, sigmaColor=75, sigmaSpace=75)
    
    # 4. Enhance contrast using CLAHE
    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8,8))
    contrast = clahe.apply(filtered)
    
    # 5. Non-linear gamma curve to separate skin (bright/clean) from dark features (glasses, hair, beard, suit)
    # Skin in portrait is around 140-220 brightness. We want skin to be very light (> 230).
    gamma = 1.6
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
    adjusted = cv2.LUT(contrast, table)
    
    # Background in original photo is white/light gray (> 210) -> force to pure 255 (white = spaces)
    adjusted[adjusted > 190] = 255
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    cv2.imwrite(output_path, adjusted)
    print("Processed portrait saved.")

if __name__ == "__main__":
    process_portrait("photo/portrait-professionnel (1).png", "data/source-prepped.png")
