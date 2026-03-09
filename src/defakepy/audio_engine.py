import numpy as np

class AudioEngine:
    """
    Engine for detecting AI-cloned voices using spectral analysis:
    Spectral Centroid (brightness) and MFCCs (vocal tract consistency).
    """
    def __init__(self, sample_rate=22050):
        self.sr = sample_rate

    def analyze_voice(self, file_path):
        """
        Analyzes an audio file for synthetic patterns.
        """
        # Lazy load librosa
        import librosa
        
        try:
            # 1. Load the audio file
            y, sr = librosa.load(file_path, sr=self.sr)

            # 2. Extract Spectral Centroid (Brightness)
            # AI often has 'robotic' consistency in brightness
            cent = librosa.feature.spectral_centroid(y=y, sr=sr)
            
            # 3. Extract MFCCs (Vocal Tract Shape)
            mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
            
            # 4. Calculate Variance
            # Real humans have higher variance (more 'jitter' and 'shimmer')
            centroid_variance = np.var(cent)
            mfcc_variance = np.var(mfccs)

            # Basic Logic: If variance is extremely low, flag as synthetic
            # Thresholds are indicative and would be tuned with a dataset
            is_synthetic = centroid_variance < 50000
            
            return {
                "is_synthetic": is_synthetic,
                "brightness_stability": 1 / (centroid_variance + 1e-6),
                "vocal_tract_consistency": mfcc_variance,
                "confidence": min(100, max(0, (50000 - centroid_variance) / 500)) if is_synthetic else 0
            }
        except Exception as e:
            return {"error": str(e)}

    def analyze(self, file_path):
        """Unified analysis for audio."""
        return self.analyze_voice(file_path)
