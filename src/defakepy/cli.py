import argparse
import sys
import json
from defakepy import ForensicScanner

def main():
    parser = argparse.ArgumentParser(
        description="🛡️ Defakepy: Open Source Deepfake & AI Detection CLI"
    )
    parser.add_argument(
        "--input", 
        "-i", 
        required=True, 
        help="Path to the file (image, video, audio, or text) to analyze"
    )
    parser.add_argument(
        "--json", 
        action="store_true", 
        help="Output results in JSON format"
    )
    parser.add_argument(
        "--version", 
        action="store_true", 
        help="Show version info"
    )

    args = parser.parse_args()

    if args.version:
        from defakepy import __version__
        print(f"Defakepy v{__version__}")
        return

    scanner = ForensicScanner()
    
    try:
        report = scanner.scan_file(args.input)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    if args.json:
        print(json.dumps(report, indent=4))
    else:
        print("\n" + "="*40)
        print("🛡️  DEFAKEPY FORENSIC REPORT")
        print("="*40)
        print(f"File:        {report['file_path']}")
        print(f"Type:        {report['type'].upper()}")
        print(f"Provenance:  {report['provenance']}")
        print(f"Trust Score: {report['trust_score']}/100")
        print("-" * 40)
        
        status = "CLEAR" if report['trust_score'] > 70 else "SUSPICIOUS" if report['trust_score'] > 40 else "CRITICAL"
        print(f"STATUS:      {status}")
        
        if report['flags']:
            print("\nFLAGS:")
            for flag in report['flags']:
                print(f"  [!] {flag}")
        
        print("="*40 + "\n")

if __name__ == "__main__":
    main()
