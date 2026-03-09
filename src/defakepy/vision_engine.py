import numpy as np

class VisionEngine:
    """
    Engine for detecting deepfakes using biological signals:
    Eye Aspect Ratio (EAR) for blinking patterns.
    """
    def __init__(self, predictor_path="shape_predictor_68_face_landmarks.dat"):
        self.predictor_path = predictor_path
        self._detector = None
        self._predictor = None

    def _load_models(self):
        """Lazy load dlib models."""
        if self._detector is None:
            import dlib
            self._detector = dlib.get_frontal_face_detector()
            try:
                self._predictor = dlib.shape_predictor(self.predictor_path)
            except Exception as e:
                print(f"Warning: Could not load dlib shape predictor from {self.predictor_path}. {e}")

    def calculate_ear(self, eye):
        """Computes the Eye Aspect Ratio (EAR)."""
        from scipy.spatial import distance as dist
        # Compute the vertical distances
        A = dist.euclidean(eye[1], eye[5])
        B = dist.euclidean(eye[2], eye[4])
        # Compute the horizontal distance
        C = dist.euclidean(eye[0], eye[3])
        # EAR Formula
        return (A + B) / (2.0 * C)

    def analyze_video(self, video_path):
        """Tracks blinking across video frames."""
        import cv2
        self._load_models()
        if self._predictor is None:
            return {"error": "Dlib predictor not loaded. Please provide shape_predictor_68_face_landmarks.dat"}

        cap = cv2.VideoCapture(video_path)
        blink_count = 0
        closed_frames = 0
        frame_count = 0
        
        # EAR threshold (standard is around 0.2 - 0.3)
        EAR_THRESHOLD = 0.2
        CONSEC_FRAMES = 2

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret: break
            frame_count += 1
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self._detector(gray)
            
            for face in faces:
                landmarks = self._predictor(gray, face)
                
                # Extract left and right eye coordinates
                # Points 36-41 (left), 42-47 (right)
                left_eye = np.array([(landmarks.part(i).x, landmarks.part(i).y) for i in range(36, 42)])
                right_eye = np.array([(landmarks.part(i).x, landmarks.part(i).y) for i in range(42, 48)])
                
                left_ear = self.calculate_ear(left_eye)
                right_ear = self.calculate_ear(right_eye)
                
                avg_ear = (left_ear + right_ear) / 2.0
                
                if avg_ear < EAR_THRESHOLD:
                    closed_frames += 1
                else:
                    if closed_frames >= CONSEC_FRAMES:
                        blink_count += 1
                    closed_frames = 0
                    
        cap.release()
        
        # Heuristic: A 30-second video should have ~5-10 blinks.
        # If 0 blinks are detected in a significant duration, it's highly suspicious.
        is_suspicious = blink_count == 0 and frame_count > 100
        
        return {
            "blink_count": blink_count,
            "frame_count": frame_count,
            "is_suspicious": is_suspicious,
            "confidence": 90 if is_suspicious else 0
        }

    def analyze(self, video_path):
        """Unified analysis for vision/video."""
        return self.analyze_video(video_path)
