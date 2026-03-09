__version__ = "0.1.6"

class ForensicScanner:
    """
    Main entry point for Defakepy.
    Unified API for Text, Audio, Video, and Image analysis.
    """
    def __init__(self):
        self._text_engine = None
        self._audio_engine = None
        self._vision_engine = None
        self._image_engine = None

    @property
    def text_engine(self):
        if self._text_engine is None:
            from .text_engine import TextEngine
            self._text_engine = TextEngine()
        return self._text_engine

    @property
    def audio_engine(self):
        if self._audio_engine is None:
            from .audio_engine import AudioEngine
            self._audio_engine = AudioEngine()
        return self._audio_engine

    @property
    def vision_engine(self):
        if self._vision_engine is None:
            from .vision_engine import VisionEngine
            self._vision_engine = VisionEngine()
        return self._vision_engine

    @property
    def image_engine(self):
        if self._image_engine is None:
            from .image_engine import ImageEngine
            self._image_engine = ImageEngine()
        return self._image_engine

    def scan_file(self, file_path):
        """
        Unified scan function that detects file type and runs appropriate engine.
        """
        import os
        ext = os.path.splitext(file_path)[1].lower()
        
        report = {
            "file_path": file_path,
            "type": "unknown",
            "trust_score": 100,
            "flags": [],
            "results": {}
        }

        # Handle Images
        if ext in ['.jpg', '.jpeg', '.png', '.webp', '.bmp']:
            report["type"] = "image"
            res = self.image_engine.analyze(file_path)
            report["results"]["image"] = res
            if res.get("is_ai"):
                report["trust_score"] -= res.get("confidence", 0)
                report["flags"].append(f"Visual Anomaly: AI-Generated Image ({res.get('confidence', 0)}% confidence)")

        # Handle Text
        elif ext in ['.txt', '.pdf', '.docx']:
            report["type"] = "text"
            pass

        # Handle Video
        elif ext in ['.mp4', '.mov', '.avi']:
            report["type"] = "video"
            res = self.vision_engine.analyze(file_path)
            report["results"]["vision"] = res
            if res.get("is_suspicious"):
                report["trust_score"] -= res.get("confidence", 0)
                report["flags"].append("Biological Anomaly: Low/Zero Blink Rate")

            # Also check audio if it's video
            audio_res = self.audio_engine.analyze(file_path)
            report["results"]["audio"] = audio_res
            if audio_res.get("is_synthetic"):
                report["trust_score"] -= audio_res.get("confidence", 0)
                report["flags"].append("Audio Anomaly: Synthetic Spectral Signature")

        # Handle Audio
        elif ext in ['.wav', '.mp3', '.m4a']:
            report["type"] = "audio"
            res = self.audio_engine.analyze(file_path)
            report["results"]["audio"] = res
            if res.get("is_synthetic"):
                report["trust_score"] -= res.get("confidence", 0)
                report["flags"].append("Audio Anomaly: Synthetic Spectral Signature")

        # Digital Provenance (Mock C2PA)
        report["provenance"] = self._check_c2pa(file_path)
        if report["provenance"] == "Unsigned":
            report["trust_score"] -= 10
            report["flags"].append("Metadata Trace: Missing C2PA/Digital Signature")

        report["trust_score"] = max(0, report["trust_score"])
        return report

    def _check_c2pa(self, file_path):
        """Check for C2PA metadata."""
        try:
            import json
            import c2pa_python as c2pa
            with c2pa.Reader(file_path) as reader:
                # Basic validation
                return "Signed"
        except:
            return "Unsigned"
