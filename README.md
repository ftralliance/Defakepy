# 🛡️ Defakepy: Open Source Deepfake & AI Detection Library

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

**Defakepy** is a powerful open-source forensic suite designed to detect AI-generated content across text, audio, and video. It provides a deterministic and statistical "Trust Score" to help verify digital reality.

---

## ✨ Key Features

- **Text Forensics:** Analyzes Perplexity and Burstiness to detect LLM-generated prose (GPT-4, Llama 3, Claude 3.5).
- **Video Biological Tells:** Uses Computer Vision to track Eye Aspect Ratio (EAR) for unnatural blinking patterns.
- **Audio Spectral Analysis:** Detects "robotic" frequency signatures in cloned voices using Mel-Frequency Cepstral Coefficients (MFCCs).
- **C2PA Metadata:** Native support for reading digital provenance signatures and manifests.
- **Lazy Loading:** High-performance CLI that only loads heavy ML models on demand.

---

## 🚀 Quick Start

### Installation
Install the core library via pip:
```bash
pip install defakepy
```

### Basic Usage (CLI)
Scan any file directly from your terminal:
```bash
defakepy-scan --input suspicious_video.mp4
```

### Python API
Integrate Defakepy into your own application:
```python
from defakepy import ForensicScanner

scanner = ForensicScanner()
report = scanner.scan_file("document.pdf")

print(f"Trust Score: {report['trust_score']}/100")
```

---

## 📊 How it Works
Defakepy uses an Ensemble Approach:
1. **Statistical Layer:** Checks for patterns AI cannot easily hide (rhythm, entropy).
2. **Biological Layer:** Checks for human-specific involuntary movements (blinking).
3. **Cryptographic Layer:** Verifies digital watermarks and C2PA signatures.

⚖️ **Legal & Ethical Disclaimer**: Detection is probabilistic, not absolute. Defakepy is a tool to assist human verification, not replace it.

🤝 **Contributing**: We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

📄 **License**: Distributed under the MIT License. See [LICENSE](LICENSE) for more information.
