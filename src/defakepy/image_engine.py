class ImageEngine:
    """
    Engine for detecting AI-generated images.

    Uses the 'umm-maybe/AI-image-detector' Vision Transformer (ViT) model from HuggingFace,
    fine-tuned to classify images as Real or AI-generated.

    The model supports common image formats: .jpg, .jpeg, .png, .webp, .bmp

    Note: This model is best at detecting GAN and diffusion-based images (Stable Diffusion,
    Midjourney, DALL-E, etc.). Highly post-processed or steganographically obfuscated images
    may still evade detection. Always treat the score as a signal, not a verdict.
    """

    MODEL_NAME = "umm-maybe/AI-image-detector"

    def __init__(self):
        self._pipeline = None

    def _load_models(self):
        """Lazy load the ViT pipeline on first use."""
        if self._pipeline is None:
            try:
                from transformers import pipeline
            except ImportError:
                raise ImportError(
                    "transformers is not installed. To use image analysis, "
                    "install with: pip install 'defakepy[image]'"
                )
            try:
                from PIL import Image  # noqa: F401
            except ImportError:
                raise ImportError(
                    "Pillow is not installed. To use image analysis, "
                    "install with: pip install 'defakepy[image]'"
                )
            print(f"Loading AI image detection model ({self.MODEL_NAME})...")
            self._pipeline = pipeline("image-classification", model=self.MODEL_NAME)

    def analyze(self, image_path: str) -> dict:
        """
        Analyze an image file and return the probability that it is AI-generated.

        Args:
            image_path: Path to the image file (.jpg, .png, .webp, etc.)

        Returns:
            dict with keys:
              - ai_probability (float): 0.0 = real, 1.0 = AI-generated
              - is_ai (bool): True if probability exceeds 60%
              - confidence (int): 0-100 confidence score
              - label (str): Raw model label ('artificial' or 'real')
        """
        self._load_models()

        try:
            from PIL import Image
            img = Image.open(image_path).convert("RGB")
        except FileNotFoundError:
            return {"error": f"File not found: {image_path}"}
        except Exception as e:
            return {"error": f"Could not open image: {e}"}

        try:
            results = self._pipeline(img)
        except Exception as e:
            return {"error": f"Model inference failed: {e}"}

        # Parse results: model outputs a list of dicts [{label, score}, ...]
        ai_prob = 0.0
        label = "unknown"
        for r in results:
            if r["label"].lower() in ("artificial", "fake", "ai"):
                ai_prob = r["score"]
                label = r["label"]
                break
            elif r["label"].lower() in ("real", "human"):
                ai_prob = 1.0 - r["score"]
                label = "artificial" if ai_prob > 0.5 else r["label"]
                break

        is_ai = ai_prob > 0.60

        return {
            "ai_probability": round(ai_prob, 4),
            "is_ai": is_ai,
            "confidence": int(ai_prob * 100),
            "label": label
        }
