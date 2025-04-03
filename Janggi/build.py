#how to create the mac executable. call python3 build.py build
#created by Andrew Nicholson

from cx_Freeze import setup, Executable
import os
import sys
import subprocess

# Determine base for executable (None for console, "Win32GUI" for GUI)
base = None
if sys.platform == "win32":
    base = None  # Or "Win32GUI" if it's a GUI app

executables = [Executable("main.py", base=base)]


image_directories = ["Board", "Pieces", "UI"]  # Add all your image directories here
include_files = [("stockfish", "stockfish"), ("Settings/settings.txt", "Settings")] 

for image_dir in image_directories:
    destination = image_dir  # Destination directory within the frozen app is the same as the source directory
    if os.path.exists(image_dir): #check if directory exists
      for filename in os.listdir(image_dir):
          if filename.endswith((".png", ".jpg", ".jpeg", ".gif")):
              full_path = os.path.join(image_dir, filename)
              include_files.append((full_path, destination))
    else:
      print(f"Warning: Directory '{image_dir}' not found.")

setup(
    name="StockfishRunner",  # Replace with your app name
    version="1.0",
    description="Runs Stockfish",
    executables=executables,
    options={
        "build_exe": {
            "include_files": include_files,
            "packages": [],  # Add any other packages your script uses
            "include_msvcr": True if sys.platform == "win32" else False, # Include MSVCR on Windows.
        },
    },
)

