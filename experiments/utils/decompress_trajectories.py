import os
import sys
import gzip
import json
import glob

def decompress_json_files(directory="."):
    """
    Decompresses all .json.gz files in the specified directory back to .json format
    
    Args:
        directory (str): Directory path to search for .json.gz files (defaults to current directory)
    """
    # Find all .json.gz files in the directory
    gz_files = glob.glob(os.path.join(directory, "*.json.gz"))
    
    if not gz_files:
        print("No .json.gz files found in the specified directory.")
        return
    
    for gz_file in gz_files:
        try:
            # Create the decompressed file path (remove .gz extension)
            json_file = gz_file[:-3]  # Remove the '.gz' extension
            
            # Read the compressed file and decompress it
            with gzip.open(gz_file, 'rb') as f:
                compressed_data = f.read()
            
            # Decode the bytes to string and load as JSON to validate
            json_str = compressed_data.decode('utf-8')
            data = json.loads(json_str)
            
            # Write the decompressed data to a new JSON file
            with open(json_file, 'w') as f:
                json.dump(data, f)
            
            # Get file sizes for comparison
            compressed_size = os.path.getsize(gz_file)
            decompressed_size = os.path.getsize(json_file)
            expansion = (decompressed_size/compressed_size - 1) * 100
            
            print(f"Decompressed {gz_file}:")
            print(f"Compressed size: {compressed_size/1024:.2f} KB")
            print(f"Decompressed size: {decompressed_size/1024:.2f} KB")
            print(f"Size expansion: {expansion:.1f}%\n")
            
            # Optionally, remove the compressed file
            os.remove(gz_file)
            
        except Exception as e:
            print(f"Error processing {gz_file}: {str(e)}")

if __name__ == "__main__":
    # Use directory from command line argument if provided, otherwise use current directory
    directory = sys.argv[1] if len(sys.argv) > 1 else "."
    decompress_json_files(directory)