from defakepy import ForensicScanner

def run_demo():
    print("--- Defakepy API Demo ---")
    scanner = ForensicScanner()

    # 1. Analyze Text
    sample_text = "In the contemporary era of technological advancement, it is important to consider the ramifications of AI."
    print(f"\nAnalyzing Raw Text...")
    text_results = scanner.text_engine.analyze(sample_text)
    print(f"Perplexity: {text_results['perplexity']:.2f}")
    print(f"Burstiness: {text_results['burstiness']:.2f}")
    print(f"Likely AI:  {text_results['is_ai']}")

    # 2. Analyze a (hypothetical) file
    # In a real scenario, you'd provide a path to an .mp4 or .wav
    print(f"\nNote: To test Video/Audio, run the CLI with real media:")
    print(f"  defakepy-scan --input path/to/media.mp4")

if __name__ == "__main__":
    run_demo()
