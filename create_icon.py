"""
Convert 1.png to app_icon.ico
Script to create Windows icon from PNG image
"""

from PIL import Image
import os

def create_icon_from_png(png_path, ico_path):
    """
    Convert PNG to ICO with multiple sizes
    """
    print(f"Converting {png_path} to {ico_path}...")
    
    try:
        # Open the PNG image
        img = Image.open(png_path)
        
        # Convert to RGBA if needed
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Create icon with multiple sizes
        icon_sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
        
        # Resize and save as ICO
        img.save(ico_path, format='ICO', sizes=icon_sizes)
        
        print(f"✓ Icon created successfully: {ico_path}")
        print(f"  Sizes: {', '.join([f'{s[0]}x{s[1]}' for s in icon_sizes])}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error creating icon: {e}")
        return False

if __name__ == "__main__":
    # Paths
    png_file = "1.png"
    ico_file = "app_icon.ico"
    
    # Check if PNG exists
    if not os.path.exists(png_file):
        print(f"✗ Error: {png_file} not found!")
        print("  Please make sure 1.png is in the current directory.")
        exit(1)
    
    # Create icon
    success = create_icon_from_png(png_file, ico_file)
    
    if success:
        print("\n✓ Done! You can now build the application with the new icon.")
        print("  Run: python build.py all")
    else:
        print("\n✗ Failed to create icon.")
        print("  Make sure Pillow is installed: pip install pillow")
