import os
import cv2
import numpy as np

def prep_portrait_photo(input_path, output_path):
    img = cv2.imread(input_path)
    if img is None:
        raise FileNotFoundError(f"Could not load {input_path}")
        
    h, w, _ = img.shape
    
    # 1. Crop to focus on head and upper chest for maximum facial resolution
    crop_top = int(h * 0.04)
    crop_bottom = int(h * 0.82)
    crop_left = int(w * 0.12)
    crop_right = int(w * 0.88)
    cropped = img[crop_top:crop_bottom, crop_left:crop_right]
    
    # 2. Convert to grayscale
    gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
    
    # 3. Bilateral Filter to smooth skin noise while preserving sharp feature edges (glasses, eyes, beard)
    filtered = cv2.bilateralFilter(gray, d=7, sigmaColor=50, sigmaSpace=50)
    
    # 4. Boost local contrast with CLAHE (Contrast-Limited Adaptive Histogram Equalization)
    clahe = cv2.createCLAHE(clipLimit=3.5, tileGridSize=(8,8))
    enhanced = clahe.apply(filtered)
    
    # 5. Extract Canny edges for critical facial features (glasses frame, eyes, eyebrows, beard line, tie)
    edges = cv2.Canny(filtered, 40, 120)
    
    # 6. Combine enhanced image with edges to make facial features stand out sharply in ASCII
    combined = enhanced.copy()
    combined[edges > 0] = np.minimum(combined[edges > 0], 30) # Force facial edges to be dark
    
    # 7. Isolate background: photo background is light gray/white (> 200) -> force to pure 255 (white = space " ")
    bg_mask = (cropped[:, :, 0] > 195) & (cropped[:, :, 1] > 195) & (cropped[:, :, 2] > 195)
    combined[bg_mask] = 255
    
    # Stretch skin tones (140-200) towards brighter end so skin is clean with subtle dots
    skin_mask = (combined >= 130) & (combined < 240)
    combined[skin_mask] = np.clip(combined[skin_mask] * 1.15, 130, 245).astype(np.uint8)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    cv2.imwrite(output_path, combined)
    print(f"Prepped portrait saved to {output_path}")

if __name__ == "__main__":
    prep_portrait_photo(os.path.join("photo", "portrait-professionnel (1).png"), os.path.join("data", "source-prepped.png"))
