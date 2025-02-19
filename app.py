import argparse
import os
import magic
import sys
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--uploaded_file', required=True, help='Input file name from inputs directory')
    args = parser.parse_args()
    
    # Construct full input path and validate
    input_path = Path('inputs').joinpath(args.uploaded_file).resolve()
    inputs_dir = Path('inputs').resolve()
    
    # Security check - ensure file is within inputs directory
    if not input_path.parent.samefile(inputs_dir):
        print(f"Error: File path must be within the inputs directory")
        sys.exit(1)
    
    # Check if input file exists
    if not input_path.exists():
        print(f"Error: Input file '{input_path}' does not exist")
        sys.exit(1)

    try:
        # Detect file type using magic numbers
        mime = magic.Magic(mime=True)
        file_type = mime.from_file(str(input_path))
        
        print(f"File type detected: {file_type}")
        return 0
        
    except magic.MagicException as e:
        print(f"Magic library error: {str(e)}")
        return 1
    except ImportError as e:
        if 'magic' in str(e):
            print("Please install python-magic first: pip install python-magic")
            if os.name == 'nt':  # Windows
                print("On Windows, you'll also need to install python-magic-bin: pip install python-magic-bin")
            return 1
        raise e
    except Exception as e:
        print(f"Error detecting file type: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())