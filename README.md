# 🛡️ Defakepy: Open Source Deepfake & AI Detection Library

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![PyPI version](https://img.shields.io/pypi/v/defakepy.svg)](https://pypi.org/project/defakepy/)

**Defakepy** is a powerful, open-source forensic suite for detecting AI-generated content across **text**, **audio**, and **video**. It uses an ensemble of statistical, biological, and cryptographic techniques to produce a human-readable **Trust Score**.

> ⚖️ **Disclaimer**: Detection is probabilistic, not absolute. Defakepy is a tool to assist human judgment, not replace it.

---

## ✨ Key Features

| Feature | Method | Detects |
|---|---|---|
| **Text Forensics** | RoBERTa binary classifier | LLM-generated prose (GPT-4, Claude, Llama) |
| **Image Analysis** | ViT (Vision Transformer) classifier | AI-generated images (Midjourney, DALL-E, SD) |
| **Video Analysis** | Eye Aspect Ratio (EAR) | Unnatural blinking in face videos |
| **Audio Forensics** | MFCC Spectral Analysis | AI voice cloning & synthetic speech |
| **Provenance Check** | C2PA Metadata | Missing/invalid digital watermarks |

---

## 🚀 Installation

Defakepy is **"Lite by Default"** — the core package is tiny and installs instantly. Install only the features you need.

### Core (Instant)
```bash
pip install defakepy
```

### Feature Extras
Install only what your use case requires:

| Extra | Command | What it enables |
|---|---|---|
| Text | `pip install "defakepy[text]"` | torch + transformers for text AI detection |
| **Image** | `pip install "defakepy[image]"` | **ViT classifier for AI image detection** |
| Audio | `pip install "defakepy[audio]"` | librosa + scipy for cloned voice detection |
| Vision | `pip install "defakepy[vision]"` | dlib + opencv for deepfake video detection |
| Provenance | `pip install "defakepy[provenance]"` | c2pa-python for digital signature checks |
| **Full** | `pip install "defakepy[full]"` | **Everything above combined** |

---

## � Usage

### 1. Python API

#### Analyze a String of Text
```python
from defakepy import ForensicScanner

scanner = ForensicScanner()

text = """Artificial intelligence has rapidly transformed numerous industries,
offering unprecedented efficiencies and capabilities that were unimaginable before."""

report = scanner.text_engine.analyze(text)

print(f"AI Generated:    {report['is_ai']}")
print(f"AI Probability:  {report['ai_probability'] * 100:.1f}%")  # e.g., 87.3%
print(f"Burstiness:      {report['burstiness']:.2f}")  # Sentence variety
print(f"Confidence:      {report['confidence']}%")
```

#### Analyze an Image File
```python
scanner = ForensicScanner()
report = scanner.image_engine.analyze("suspicious_photo.jpg")

print(f"AI Generated:   {report['is_ai']}")
print(f"AI Probability: {report['ai_probability'] * 100:.1f}%")
print(f"Confidence:     {report['confidence']}%")
```

#### Analyze an Audio File
```python
scanner = ForensicScanner()
report = scanner.audio_engine.analyze("voice_clip.wav")

print(f"Synthetic Voice: {report['is_synthetic']}")
print(f"Confidence:      {report['confidence']}%")
```

#### Analyze a Video File
```python
scanner = ForensicScanner()
report = scanner.vision_engine.analyze("interview.mp4")

print(f"Suspicious:  {report['is_suspicious']}")
print(f"Blink Count: {report['blink_count']}")
print(f"Confidence:  {report['confidence']}%")
```

#### All-in-One File Scan
Automatically detects file type and runs the appropriate engine:
```python
scanner = ForensicScanner()
report = scanner.scan_file("suspicious_video.mp4")

print(f"Trust Score: {report['trust_score']}/100")
print(f"Status:      {'CLEAR' if report['trust_score'] > 70 else 'SUSPICIOUS'}")
for flag in report.get('flags', []):
    print(f"  [!] {flag}")
```

---

### 2. Command-Line Interface (CLI)

#### Basic Scan
```bash
defakepy-scan --input suspicious_video.mp4
```

#### Output as JSON (for scripting/automation)
```bash
defakepy-scan --input my_article.txt --json
```

#### Check Version
```bash
defakepy-scan --version
```

#### Example CLI Output
```
========================================
🛡️  DEFAKEPY FORENSIC REPORT
========================================
File:        suspicious_video.mp4
Type:        VIDEO
Provenance:  Unsigned
Trust Score: 45/100
----------------------------------------
STATUS:      SUSPICIOUS

FLAGS:
  [!] Biological Anomaly: Low/Zero Blink Rate
  [!] Audio Anomaly: Synthetic Spectral Signature
  [!] Metadata Trace: Missing C2PA/Digital Signature
========================================
```

---

## 📊 Understanding the Output

### Trust Score
- **> 70 → ✅ CLEAR**: No significant anomalies found.
- **40–70 → ⚠️ SUSPICIOUS**: One or more anomalies detected. Review recommended.
- **< 40 → 🚨 CRITICAL**: Multiple strong indicators of AI generation or manipulation.

### Text Analysis: `ai_probability`
The text engine returns an `ai_probability` score (0.0 = human, 1.0 = AI), powered by a fine-tuned **RoBERTa classifier** (`Hello-SimpleAI/chatgpt-detector-roberta`). A result > 60% is flagged as AI.

> ⚠️ **Limitation**: AI text detection is still an open research problem. Adversarial prompting (e.g., "rewrite this to sound more human"), paraphrasing tools, or fine-tuned models can evade any classifier. Treat the result as a signal to investigate further, not a verdict.

### Flags Explained
| Flag | What it Means |
|---|---|
| `Biological Anomaly: Low/Zero Blink Rate` | A real human blinks 15–20 times per minute. AI-generated videos often have zero or near-zero blinks. |
| `Audio Anomaly: Synthetic Spectral Signature` | Real voices have natural variation and imperfections. Cloned voices are spectrally "too smooth." |
| `Metadata Trace: Missing C2PA/Digital Signature` | Authentic media from cameras/publishers carries a C2PA watermark. Its absence is a weak signal but worth flagging. |

---

## 🛠️ Troubleshooting

### `ReadTimeoutError` during installation
Your network timed out while downloading a large file. Run with an extended timeout:
```bash
pip install --default-timeout=1000 "defakepy[full]"
```

### `dlib` build failure on Windows
`dlib` requires **CMake** and a C++ compiler. Install CMake from [cmake.org](https://cmake.org/download/), select **"Add CMake to the system PATH"**, restart your terminal, then try again.

### `ImportError: torch is not installed`
You're using a feature without its required extra. Fix:
```bash
pip install "defakepy[text]"    # for text analysis
pip install "defakepy[image]"   # for image analysis
pip install "defakepy[audio]"   # for audio analysis
pip install "defakepy[vision]"  # for video analysis
pip install "defakepy[full]"    # for everything
```

### `OSError: [WinError 1114]` DLL Initialization Failed (Windows)
This happens when **PyTorch's C++ runtime libraries** can't load because the **Microsoft Visual C++ Redistributable** is missing.

1. Download and install it: **[https://aka.ms/vs/17/release/vc_redist.x64.exe](https://aka.ms/vs/17/release/vc_redist.x64.exe)**
2. **Restart your computer.**
3. Try again.

Alternatively, use the lighter CPU-only torch version which has fewer DLL dependencies:
```bash
pip uninstall torch
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

---

## 🤝 Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) to get started.

## 📄 License

Distributed under the MIT License. See [LICENSE](LICENSE) for details.
