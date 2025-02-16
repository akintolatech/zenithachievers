import os
import zipfile
import datetime

# Define the name of the zip file with a timestamp
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
zip_filename = f"app_{timestamp}.zip"

# Directories to exclude
exclude_dirs = {'.git', '.idea', '.venv'}

# Create a ZipFile object in write mode
with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk('.'):
        # Exclude the directories listed
        dirs[:] = [d for d in dirs if d not in exclude_dirs]

        # Add files to the zip file
        for file in files:
            file_path = os.path.join(root, file)
            zipf.write(file_path, os.path.relpath(file_path, start='.'))

print(f"Everything zipped into {zip_filename}")
