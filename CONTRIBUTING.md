# Contributing to Defakepy

First off, thank you for considering contributing to Defakepy! It's people like you that make the internet a safer place.

## How Can I Contribute?

### 1. Reporting Bugs
- Use the GitHub Issue Tracker.
- Provide a clear description and, if possible, the file that caused the error.

### 2. Suggesting Enhancements
- We are always looking for new "tells" (e.g., skin texture analysis, lip-sync mismatch).
- Open an issue with the tag `enhancement`.

### 3. Pull Requests
1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests!
3. Ensure your code follows PEP 8.
4. Issue that Pull Request!

## Development Environment Setup
1. Clone your fork.
2. Create a virtual environment: `python -m venv venv`
3. Install in editable mode with dev dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

## Our Philosophy
We prioritize **Explainability**. A detection score is useless without a reason. Always aim to provide a "why" alongside a "what."
