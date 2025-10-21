import os
import sys
import gzip
import json
import glob

def compress_json_files(directory="."):
    """
    Compresses all JSON files in the specified directory to .json.gz format
    
    Args:
        directory (str): Directory path to search for JSON files (defaults to current directory)
    """
    # Find all .json files in the directory
    json_files = glob.glob(os.path.join(directory, "*.json"))
    
    if not json_files:
        print("No JSON files found in the specified directory.")
        return
    
    for json_file in json_files:
        try:
            # Read the original JSON file
            with open(json_file, 'r') as f:
                data = json.load(f)
            
            # Create the gzipped file path
            gz_file = json_file + '.gz'
            
            # Write the compressed file
            with gzip.open(gz_file, 'wb') as f:
                # Convert JSON to string and encode to bytes before writing
                json_str = json.dumps(data)
                f.write(json_str.encode('utf-8'))
            
            # Get file sizes for comparison
            original_size = os.path.getsize(json_file)
            compressed_size = os.path.getsize(gz_file)
            savings = (1 - compressed_size/original_size) * 100
            
            print(f"Compressed {json_file}:")
            print(f"Original size: {original_size/1024:.2f} KB")
            print(f"Compressed size: {compressed_size/1024:.2f} KB")
            print(f"Space savings: {savings:.1f}%\n")
            
            # Optionally, remove the original file
            os.remove(json_file)
            
        except json.JSONDecodeError:
            print(f"Error: {json_file} is not a valid JSON file")
        except Exception as e:
            print(f"Error processing {json_file}: {str(e)}")

if __name__ == "__main__":
    compress_json_files(sys.argv[1])