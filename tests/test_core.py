import pytest
import os
from defakepy import ForensicScanner

def test_scanner_initialization():
    """Test that the ForensicScanner can be initialized."""
    scanner = ForensicScanner()
    assert scanner is not None

def test_text_engine_lazy_loading():
    """Test that the text engine is only loaded when accessed."""
    scanner = ForensicScanner()
    assert scanner._text_engine is None
    _ = scanner.text_engine
    assert scanner._text_engine is not None

def test_audio_engine_lazy_loading():
    """Test that the audio engine is only loaded when accessed."""
    scanner = ForensicScanner()
    assert scanner._audio_engine is None
    _ = scanner.audio_engine
    assert scanner._audio_engine is not None

def test_vision_engine_lazy_loading():
    """Test that the vision engine is only loaded when accessed."""
    scanner = ForensicScanner()
    assert scanner._vision_engine is None
    _ = scanner.vision_engine
    assert scanner._vision_engine is not None

def test_scan_file_type_detection():
    """Test that scan_file identifies common extensions correctly."""
    scanner = ForensicScanner()
    
    # Text
    report = scanner.scan_file("test.txt")
    assert report["type"] == "text"
    
    # Video
    report = scanner.scan_file("test.mp4")
    assert report["type"] == "video"
    
    # Audio
    report = scanner.scan_file("test.wav")
    assert report["type"] == "audio"
