import pytesseract
from PIL import Image, ImageFilter, ImageEnhance, ImageOps

import os
import shutil

# ✅ Specify Tesseract path (Check env var first, then common paths)
TESSERACT_PATH = os.getenv("TESSERACT_PATH", r'C:\Program Files\Tesseract-OCR\tesseract.exe')

if not os.path.exists(TESSERACT_PATH):
    # Try to find in PATH
    tess_in_path = shutil.which("tesseract")
    if tess_in_path:
        TESSERACT_PATH = tess_in_path
    else:
        print(f"[WARNING] Tesseract not found at {TESSERACT_PATH}. OCR will fail.")

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

def preprocess_image(image: Image.Image) -> Image.Image:
    try:
        # Convert to grayscale
        image = image.convert('L')
        
        # Auto contrast for better sharpness
        image = ImageOps.autocontrast(image)
        
        # Slight sharpening
        image = image.filter(ImageFilter.SHARPEN)
        
        # Optional: Increase contrast slightly
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.5)

        # Optional: Resize if small image
        if image.size[0] < 600:
            image = image.resize(
                (image.size[0]*2, image.size[1]*2),
                Image.Resampling.LANCZOS  # ✅ Correct replacement for ANTIALIAS
            )
        return image
    except Exception as e:
        print(f"[ERROR] Image preprocessing failed: {e}")
        return image  # fallback to original if preprocessing fails

def extract_text_from_image(image: Image.Image) -> str:
    try:
        processed_image = preprocess_image(image)
        text = pytesseract.image_to_string(processed_image)
        return text.strip()
    except Exception as e:
        print(f"[ERROR] OCR failed: {e}")
        return "[OCR Error]"
