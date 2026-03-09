import numpy as np

class TextEngine:
    """
    Engine for detecting AI-generated text using statistical methods:
    Perplexity (predictability) and Burstiness (sentence variation).
    """
    def __init__(self, model_name='gpt2'):
        self.model_name = model_name
        self._model = None
        self._tokenizer = None

    def _load_models(self):
        """Lazy load heavy ML models only when needed."""
        if self._model is None:
            import torch
            from transformers import GPT2LMHeadModel, GPT2Tokenizer
            
            print(f"Loading {self.model_name} models for text analysis...")
            self._tokenizer = GPT2Tokenizer.from_pretrained(self.model_name)
            self._model = GPT2LMHeadModel.from_pretrained(self.model_name)
            self._model.eval()

    def get_perplexity(self, text):
        """Calculates how 'surprised' the model is by the text."""
        self._load_models()
        import torch
        
        encodings = self._tokenizer(text, return_tensors='pt')
        max_length = self._model.config.n_positions
        stride = 512
        seq_len = encodings.input_ids.size(1)

        nlls = []
        for i in range(0, seq_len, stride):
            begin_loc = max(i + stride - max_length, 0)
            end_loc = min(i + stride, seq_len)
            trg_len = end_loc - i
            input_ids = encodings.input_ids[:, begin_loc:end_loc]
            target_ids = input_ids.clone()
            target_ids[:, :-trg_len] = -100

            with torch.no_grad():
                outputs = self._model(input_ids, labels=target_ids)
                neg_log_likelihood = outputs.loss * trg_len

            nlls.append(neg_log_likelihood)

        ppl = torch.exp(torch.stack(nlls).sum() / end_loc)
        return ppl.item()

    def calculate_burstiness(self, text):
        """Calculates the standard deviation of sentence lengths."""
        sentences = text.split('.')
        lengths = [len(s.split()) for s in sentences if len(s.split()) > 0]
        if not lengths:
            return 0
        return np.std(lengths)

    def analyze(self, text):
        """Unified analysis for text."""
        ppl = self.get_perplexity(text)
        burstiness = self.calculate_burstiness(text)
        
        # Heuristic: AI text is often low perplexity (<100) and low burstiness (<5)
        # These thresholds are experimental and would normally scale with model size
        is_ai = ppl < 80 and burstiness < 5
        
        return {
            "perplexity": ppl,
            "burstiness": burstiness,
            "is_ai": is_ai,
            "confidence": min(100, max(0, (80 - ppl) + (5 - burstiness) * 10)) if is_ai else 0
        }
