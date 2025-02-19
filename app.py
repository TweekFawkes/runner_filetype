import argparse
import os
import magic
import sys
from pathlib import Path
import ctypes.util

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--uploaded_file', required=True, help='Input file name from inputs directory')
    args = parser.parse_args()
    
    try:
        print("libmagic found at:", ctypes.util.find_library("magic"))
        # Construct full input path and validate
        input_path = Path('inputs').joinpath(args.uploaded_file).resolve()
        inputs_dir = Path('inputs').resolve()
        
        # Security check - ensure file is within inputs directory
        if not input_path.parent.samefile(inputs_dir):
            print(f"Error: File path must be within the inputs directory")
            return 1
        
        # Check if input file exists
        if not input_path.exists():
            print(f"Error: Input file '{input_path}' does not exist")
            return 1

        # Detect file type using magic numbers
        try:
            mime = magic.Magic(mime=True)
            file_type = mime.from_file(str(input_path))
            print(f"File type detected: {file_type}")
            return 0
        except magic.MagicException as e:
            print(f"Error: Unable to detect file type - {str(e)}")
            return 1
        
    except ImportError as e:
        if 'libmagic' in str(e).lower():
            print("Error: Required system library 'libmagic' is missing")
            print("To install on Debian/Ubuntu: sudo apt-get update && sudo apt-get install -y libmagic1")
            print("To install on RHEL/CentOS: sudo yum install -y file-libs")
            print("To install on Alpine: apk add --no-cache file-dev")
            return 1
        elif 'magic' in str(e).lower():
            print("Error: Python package 'python-magic' is missing")
            print("To install: pip install python-magic")
            return 1
        raise e
    except Exception as e:
        print(f"Error: Unexpected error while processing file - {str(e)}")
        return 1

    

if __name__ == "__main__":
    sys.exit(main())