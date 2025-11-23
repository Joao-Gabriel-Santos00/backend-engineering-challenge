import argparse
import sys
import os
from processor import process_stream

def main():
    parser = argparse.ArgumentParser(description="Translation Delivery Time Aggregator")
    parser.add_argument("--input_file", required=True, help="Path to the JSON input file")
    parser.add_argument("--window_size", required=True, type=int, help="Window size in minutes")
    
    args = parser.parse_args()

    if not os.path.exists(args.input_file):
        print(f"Error: Input file '{args.input_file}' not found.")
        sys.exit(1)
    
    # Run the main logic
    process_stream(args.input_file, args.window_size)

if __name__ == "__main__":
    main()