import os
import sys

# --- Configuration ---
# Maximum number of lines to display for large text-based files.
MAX_LINES_TO_DISPLAY = 20

def format_file_size(size_bytes):
    """Converts a file size in bytes to a human-readable format."""
    if size_bytes == 0:
        return "0 Bytes"
    
    # 1024 bytes = 1 KB
    size_name = ("Bytes", "KB", "MB", "GB", "TB")
    i = 0
    while size_bytes >= 1024 and i < len(size_name) - 1:
        size_bytes /= 1024
        i += 1
    return f"{size_bytes:.2f} {size_name[i]}"

def view_py(filepath):
    """Views Python source code files with line numbers."""
    print("=" * 60)
    print(f"Viewing Python Source Code: {os.path.basename(filepath)}")
    print("=" * 60)
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f, 1):
                # Print line number and the line content
                print(f"{i:4d}: {line.rstrip()}")
    except IOError as e:
        print(f"ERROR: Could not read file content. {e}")

def view_3d_text_header(filepath, file_type, key_elements):
    """
    Views the header of text-based 3D model files (OBJ, MTL, PLY).
    Displays the first few lines to show the core definitions.
    """
    print("=" * 60)
    print(f"Analyzing {file_type} Model Header: {os.path.basename(filepath)}")
    print(f"Expected Key Elements: {key_elements}")
    print("=" * 60)

    line_count = 0
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                if line_count < MAX_LINES_TO_DISPLAY:
                    print(line.strip())
                    line_count += 1
                else:
                    break
        
        if line_count == MAX_LINES_TO_DISPLAY:
            print(f"\n... Displaying the first {MAX_LINES_TO_DISPLAY} lines only ...")

    except UnicodeDecodeError:
        print("\nNOTE: This file appears to be a complex or binary format.")
        print("Falling back to generic analysis.")
        view_complex_file(filepath, file_type)
    except IOError as e:
        print(f"ERROR: Could not read file content. {e}")


def view_complex_file(filepath, file_type):
    """Analyzes binary or highly complex 3D model formats (STL, DAE, X3D, X)."""
    print("=" * 60)
    print(f"Analyzing Complex/Binary File: {file_type} Model")
    print(f"File: {os.path.basename(filepath)}")
    print("=" * 60)
    
    # Check file size
    try:
        file_size = os.path.getsize(filepath)
        print(f"File Size: {format_file_size(file_size)}")
    except os.error as e:
        print(f"ERROR: Could not determine file size. {e}")
        return

    print("\nContent Preview (First 128 bytes):")
    try:
        # Read a small number of bytes to see if it's text or binary
        with open(filepath, 'rb') as f:
            preview_bytes = f.read(128)
            print(preview_bytes)
            
            # Simple check for ASCII STL or DAE/X3D XML header
            preview_str = preview_bytes.decode('utf-8', errors='ignore')
            if 'solid' in preview_str.lower() and file_type == '.stl':
                print("\n-> HINT: This looks like an ASCII (Text) STL header.")
            elif '<collada' in preview_str.lower() and file_type == '.dae':
                print("\n-> HINT: This looks like a DAE (Collada) XML header.")
            elif 'xml' in preview_str.lower() or '<x3d' in preview_str.lower():
                print(f"\n-> HINT: This file may contain XML/text data.")

    except IOError as e:
        print(f"ERROR: Could not access file for binary preview. {e}")
        return

    print(f"\nNOTE: Full viewing of {file_type} requires a dedicated 3D visualization tool.")
    print("This utility provides basic file structure and size information.")


def main():
    """Main function to handle command-line arguments and dispatch viewing."""
    if len(sys.argv) < 2:
        print("Usage: python file_viewer.py <path_to_file>")
        print("\nSupported file types: .py, .obj, .mtl, .stl, .ply, .dae, .x, .x3d")
        sys.exit(1)

    filepath = sys.argv[1]

    if not os.path.exists(filepath):
        print(f"Error: File not found at '{filepath}'")
        sys.exit(1)

    # Get the file extension and convert to lowercase for uniform comparison
    _, ext = os.path.splitext(filepath)
    ext = ext.lower()

    print(f"\n[ File View Utility ] - Analyzing file: {os.path.basename(filepath)}")
    print(f"Full Path: {filepath}")

    # Dispatch based on file extension
    if ext == '.py':
        view_py(filepath)
    elif ext == '.obj':
        view_3d_text_header(filepath, "Wavefront OBJ", "v (vertex), f (face), mtllib (material library)")
    elif ext == '.mtl':
        view_3d_text_header(filepath, "Wavefront MTL", "newmtl (material name), Kd (diffuse color), Ns (specular exponent)")
    elif ext == '.ply':
        view_3d_text_header(filepath, "Stanford PLY", "ply (header), format, element vertex, element face")
    elif ext in ['.stl', '.dae', '.x', '.x3d']:
        view_complex_file(filepath, ext)
    else:
        print("=" * 60)
        print(f"Error: Unsupported file type: {ext}")
        print("Supported types: .py, .obj, .mtl, .stl, .ply, .dae, .x, .x3d")
        print("=" * 60)

if __name__ == "__main__":
    main()

