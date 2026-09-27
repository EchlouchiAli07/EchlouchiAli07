import os
import cv2
import numpy as np

def prep_transparent_photo(input_path, output_path):
    # Read RGBA image
    img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        raise FileNotFoundError(f"Could not load {input_path}")
        
    h, w = img.shape[:2]
    
    # Check if alpha channel exists
    if img.shape[2] == 4:
        b, g, r, alpha = cv2.split(img)
    else:
        b, g, r = cv2.split(img)
        alpha = np.ones((h, w), dtype=np.uint8) * 255
        
    gray = cv2.cvtColor(cv2.merge([b, g, r]), cv2.COLOR_BGR2GRAY)
    
    # Contrast enhancement on subject using CLAHE
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    enhanced = clahe.apply(gray)
    
    # Sharp edge extraction on eyes, glasses, beard, tie
    edges = cv2.Canny(enhanced, 30, 100)
    enhanced[edges > 0] = np.minimum(enhanced[edges > 0], 20)
    
    # Composite onto pure white (255) for non-alpha background
    result = np.ones((h, w), dtype=np.uint8) * 255
    mask = alpha > 10
    result[mask] = enhanced[mask]
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    cv2.imwrite(output_path, result)
    print(f"Prepped transparent photo saved to {output_path}")

if __name__ == "__main__":
    src = os.path.join("photo", "portrait-professionnel-removebg-preview.png")
    dst = os.path.join("data", "source-prepped.png")
    prep_transparent_photo(src, dst)
