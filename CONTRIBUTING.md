# 🤝 Contributing to Defakepy

First off, thank you for contributing to Defakepy! Your work helps keep the internet more trustworthy. This document explains everything you need to know to start contributing.

---

## 📐 Project Architecture

Understanding the project structure is the first step.

```
Defakepy/
├── src/
│   └── defakepy/
│       ├── __init__.py        # ForensicScanner: the main unified API & scan_file() router
│       ├── text_engine.py     # TextEngine: RoBERTa AI text classifier
│       ├── audio_engine.py    # AudioEngine: Spectral/MFCC analysis
│       ├── vision_engine.py   # VisionEngine: Eye Aspect Ratio (blink detection)
│       ├── image_engine.py    # ImageEngine: ViT AI image classifier
│       └── cli.py             # CLI entry point (defakepy-scan command)
├── tests/
│   └── test_core.py           # Core test suite
├── examples/
│   └── basic_usage.py         # Example script for new users
├── pyproject.toml             # Package configuration & dependencies
├── README.md                  # User-facing documentation
└── CONTRIBUTING.md            # This file
```

### How the Engines Work

| Engine | File | Core Technique | Extra Required |
|---|---|---|---|
| `TextEngine` | `text_engine.py` | RoBERTa binary classifier (`chatgpt-detector-roberta`) | `defakepy[text]` |
| `ImageEngine` | `image_engine.py` | ViT binary classifier (`AI-image-detector`) | `defakepy[image]` |
| `AudioEngine` | `audio_engine.py` | Spectral Centroid Variance + MFCC | `defakepy[audio]` |
| `VisionEngine` | `vision_engine.py` | Eye Aspect Ratio (EAR) Blink Tracking | `defakepy[vision]` |
| `ForensicScanner` | `__init__.py` | Routes files to engines + adds C2PA check | `defakepy[provenance]` |

> **Important — how `scan_file()` routes files:**
> - `.txt / .pdf / .docx` → `TextEngine`
> - `.jpg / .jpeg / .png / .webp / .bmp` → `ImageEngine`
> - `.mp4 / .mov / .avi` → `VisionEngine` + `AudioEngine`
> - `.wav / .mp3 / .m4a` → `AudioEngine`

All engines use **lazy loading** — heavy models are only imported when the engine is first used. They also use **graceful degradation** — if an optional dependency is missing, a helpful `ImportError` is raised with the exact install command.

---

## 🛠️ Development Environment Setup

### 1. Fork & Clone
```bash
# Fork the repo on GitHub, then:
git clone https://github.com/YOUR-USERNAME/Defakepy.git
cd Defakepy
```

### 2. Create a Virtual Environment
```bash
python -m venv .venv

# Activate it:
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

### 3. Install in Editable Mode with All Extras
```bash
pip install -e ".[full,dev]"
```
The `-e` flag means any code changes you make are immediately reflected without reinstalling. The `dev` extra adds `pytest`, `black`, and `isort`.

### 4. Run the Tests
```bash
pytest
```

---

## 🧑‍💻 How to Contribute

### Reporting Bugs
- Open an [Issue](https://github.com/ftralliance/Defakepy/issues) using the **Bug Report** template.
- Include your OS, Python version, and a minimal example that reproduces the error.

### Suggesting a New Detection Method (Most Valuable!)
We are always looking for new "tells" — verifiable signals that distinguish AI content from human content. Here's the current state and best opportunities to contribute:

| Area | Status | Best Opportunities |
|---|---|---|
| **Text** | ✅ RoBERTa classifier | Improve with ensemble models; add multilingual support |
| **Image** | ✅ ViT classifier | Add Fourier-domain artifact analysis; test against SDXL/Flux models |
| **Audio** | ✅ MFCC spectral analysis | Add breathing pattern detection, Mel spectrogram visualization |
| **Video (Face)** | ✅ EAR blink tracking | Add lip-sync analysis (SyncNet), facial texture consistency |
| **Video (Scene)** | ❌ Not implemented | Scene-level AI detection (AI backgrounds, lighting inconsistency) |
| **Documents** | ❌ Not implemented | Read & scan text from `.pdf` and `.docx` files, not just `.txt` |
| **Metadata** | ✅ C2PA check (basic) | Improve to fully parse C2PA manifests |

Open an [Issue](https://github.com/ftralliance/Defakepy/issues) with the tag `enhancement` and describe the signal and your proposed approach.

### Improving Detection Thresholds
The confidence thresholds in each engine (`is_synthetic`, `is_ai`, `EAR_THRESHOLD`) are experimental. If you run Defakepy against a labeled benchmark dataset and find better values, please open a PR with your methodology!

### Submitting a Pull Request (PR)
1. **Create a branch** from `main`:
   ```bash
   git checkout -b feature/my-new-detection-method
   ```
2. **Make your changes.** Follow the coding conventions below.
3. **Add tests** in `tests/test_core.py`.
4. **Format your code**:
   ```bash
   black src/
   isort src/
   ```
5. **Run the tests** and make sure they pass:
   ```bash
   pytest
   ```
6. **Open the PR** against `main`. Fill in the PR template with a clear description.

---

## 📝 Coding Conventions

- **PEP 8** compliant. Use `black` for auto-formatting.
- **Lazy imports**: Keep all heavy library imports (`torch`, `cv2`, `librosa`) *inside functions*, not at module level. This preserves the "Lite by Default" architecture.
- **Graceful degradation**: Any optional engine import **must** be wrapped in a `try/except ImportError` with a clear message pointing the user to the correct `pip install "defakepy[extra]"` command.
- **Return dictionaries**: Engine `analyze()` methods must return a dictionary. Always include an `error` key if analysis fails, so the top-level `scan_file` can handle it cleanly.

**Example of the correct pattern:**
```python
def analyze_something(self, file_path):
    try:
        import some_optional_library
    except ImportError:
        raise ImportError(
            "some_optional_library is not installed. "
            "Install with: pip install 'defakepy[feature]'"
        )
    # ... rest of your code
    return {"result": ..., "confidence": ...}
```

---

## 🧭 Our Philosophy

1. **Explainability first.** A score without a reason is useless. Every detection must produce a clear, human-understandable `flag`.
2. **Caution over confidence.** We would rather report a _False Positive_ (flagging real content) than miss a _True Positive_. Make the system lean toward caution.
3. **Modular design.** Each engine is self-contained. A developer should be able to `from defakepy.audio_engine import AudioEngine` and use it standalone without needing the entire library.

---

## 📬 Questions?

Open a [Discussion](https://github.com/ftralliance/Defakepy/discussions) or email us at `ftralliance@gmail.com`.
