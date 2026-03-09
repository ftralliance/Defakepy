import numpy as np


class TextEngine:
    """
    Engine for detecting AI-generated text.

    Uses the 'Hello-SimpleAI/chatgpt-detector-roberta' model from HuggingFace,
    a RoBERTa classifier fine-tuned to detect AI-written text.

    This replaces the old GPT-2 perplexity method, which was unreliable against
    modern LLMs (GPT-4, Claude, Gemini) because they generate text that surprises
    older models, causing false negatives.

    Note: This is still an imperfect science. Adversarial prompting, paraphrasing,
    and model updates can fool any classifier. Always use this as a signal, not a verdict.
    """

    MODEL_NAME = "Hello-SimpleAI/chatgpt-detector-roberta"

    def __init__(self):
        self._model = None
        self._tokenizer = None

    def _load_models(self):
        """Lazy load the RoBERTa classifier on first use."""
        if self._model is None:
            try:
                import torch
                from transformers import AutoTokenizer, AutoModelForSequenceClassification
            except ImportError:
                raise ImportError(
                    "torch or transformers is not installed. To use text analysis, "
                    "install with: pip install 'defakepy[text]'"
                )
            print(f"Loading AI text detection model ({self.MODEL_NAME})...")
            self._tokenizer = AutoTokenizer.from_pretrained(self.MODEL_NAME)
            self._model = AutoModelForSequenceClassification.from_pretrained(self.MODEL_NAME)
            self._model.eval()

    def get_ai_probability(self, text):
        """
        Returns the probability (0.0 to 1.0) that the text is AI-generated.

        The underlying model is a binary classifier:
          - Label 0: Human-written
          - Label 1: AI-generated
        """
        self._load_models()
        try:
            import torch
        except ImportError:
            raise ImportError("torch is not installed. Install with: pip install 'defakepy[text]'")

        # Truncate text to model's max token length (512)
        inputs = self._tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=512
        )
        with torch.no_grad():
            outputs = self._model(**inputs)

        # Apply softmax to get probabilities
        probs = torch.softmax(outputs.logits, dim=-1)
        # Index 1 is the "AI-generated" class
        ai_prob = probs[0][1].item()
        return ai_prob

    def calculate_burstiness(self, text):
        """Calculates the standard deviation of sentence lengths (human heuristic)."""
        sentences = text.split('.')
        lengths = [len(s.split()) for s in sentences if len(s.split()) > 0]
        if not lengths:
            return 0
        return float(np.std(lengths))

    def analyze(self, text):
        """
        Unified analysis for text.

        Returns:
            dict with keys:
              - ai_probability (float): 0.0 = human, 1.0 = AI
              - burstiness (float): Variation in sentence length (low = AI-like)
              - is_ai (bool): True if the classifier is confident the text is AI-generated
              - confidence (int): 0-100 confidence score
        """
        ai_prob = self.get_ai_probability(text)
        burstiness = self.calculate_burstiness(text)

        # Threshold: flag as AI if the model is >60% confident
        is_ai = ai_prob > 0.60

        return {
            "ai_probability": round(ai_prob, 4),
            "burstiness": round(burstiness, 4),
            "is_ai": is_ai,
            "confidence": int(ai_prob * 100)
        }
