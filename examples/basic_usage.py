#!/usr/bin/env python3
"""
Defakepy - Basic Usage Examples
================================
Run this script to see how each engine works.

Before running, make sure you've installed the needed extras:
    pip install "defakepy[text,audio,vision]"
"""

from defakepy import ForensicScanner

scanner = ForensicScanner()

# ─────────────────────────────────────────────
# 1. TEXT ANALYSIS
# Needs: pip install "defakepy[text]"
# ─────────────────────────────────────────────
def demo_text():
    print("\n" + "="*50)
    print("📄 TEXT ANALYSIS DEMO")
    print("="*50)

    ai_text = (
        "In the contemporary era of rapid technological advancement, "
        "organizations must prioritize the strategic implementation of AI "
        "to remain competitive in the global marketplace."
    )
    human_text = (
        "I went to the market today. It was chaotic! Someone's dog knocked "
        "over a whole stand of apples. Apples everywhere. I bought some anyway."
    )

    for label, text in [("Likely AI", ai_text), ("Likely Human", human_text)]:
        result = scanner.text_engine.analyze(text)
        print(f"\n  [{label}]")
        print(f"  AI Probability: {result['ai_probability'] * 100:.1f}%  (higher = more likely AI)")
        print(f"  Burstiness:     {result['burstiness']:.2f}  (lower = more AI-like)")
        print(f"  Verdict:        {'🤖 AI' if result['is_ai'] else '✅ Human'} (Confidence: {result['confidence']}%)")


# ─────────────────────────────────────────────
# 2. AUDIO ANALYSIS
# Needs: pip install "defakepy[audio]"
# Provide an actual .wav or .mp3 file path.
# ─────────────────────────────────────────────
def demo_audio(file_path: str):
    print("\n" + "="*50)
    print("🎙️ AUDIO ANALYSIS DEMO")
    print("="*50)
    result = scanner.audio_engine.analyze(file_path)
    if "error" in result:
        print(f"  Error: {result['error']}")
    else:
        verdict = "🤖 Synthetic Voice" if result["is_synthetic"] else "✅ Real Voice"
        print(f"  File:       {file_path}")
        print(f"  Verdict:    {verdict} (Confidence: {result['confidence']}%)")


# ─────────────────────────────────────────────
# 3. VIDEO ANALYSIS
# Needs: pip install "defakepy[vision]"
# Provide an actual .mp4 or .avi file path.
# Also requires: shape_predictor_68_face_landmarks.dat
# ─────────────────────────────────────────────
def demo_video(file_path: str):
    print("\n" + "="*50)
    print("🎬 VIDEO ANALYSIS DEMO")
    print("="*50)
    result = scanner.vision_engine.analyze(file_path)
    if "error" in result:
        print(f"  Error: {result['error']}")
    else:
        verdict = "🤖 Suspicious (AI-like)" if result["is_suspicious"] else "✅ Normal Blink Rate"
        print(f"  File:        {file_path}")
        print(f"  Blink Count: {result['blink_count']} over {result['frame_count']} frames")
        print(f"  Verdict:     {verdict} (Confidence: {result['confidence']}%)")


# ─────────────────────────────────────────────
# 4. UNIFIED FILE SCAN
# Auto-detects file type and runs the right engine.
# ─────────────────────────────────────────────
def demo_scan_file(file_path: str):
    print("\n" + "="*50)
    print("🛡️ UNIFIED FILE SCAN DEMO")
    print("="*50)
    report = scanner.scan_file(file_path)

    status = "✅ CLEAR" if report["trust_score"] > 70 else "⚠️ SUSPICIOUS" if report["trust_score"] > 40 else "🚨 CRITICAL"
    print(f"  File:        {report['file_path']}")
    print(f"  Type:        {report['type'].upper()}")
    print(f"  Provenance:  {report['provenance']}")
    print(f"  Trust Score: {report['trust_score']}/100")
    print(f"  Status:      {status}")
    if report.get("flags"):
        print("  Flags:")
        for flag in report["flags"]:
            print(f"    [!] {flag}")


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
if __name__ == "__main__":
    # Run the text demo (no file needed)
    try:
        demo_text()
    except ImportError as e:
        print(f"\n  [!] {e}")

    # Uncomment below and provide real file paths to test audio/video:
    # demo_audio("path/to/voice_sample.wav")
    # demo_video("path/to/video_clip.mp4")
    # demo_scan_file("path/to/any_media.mp4")

    print("\n" + "="*50)
    print("Done! Run `defakepy-scan --input yourfile.mp4` for the CLI.")
    print("="*50 + "\n")
