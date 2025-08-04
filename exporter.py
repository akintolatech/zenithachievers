import os
import zipfile
import datetime


# Define the name of the zip file with a timestamp
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
zip_filename = f"app_{timestamp}.zip"

# Directories and files to exclude
exclude_dirs = {'.git', '.idea', '.venv',}
print(type(exclude_dirs))
exclude_files = {zip_filename}  # Exclude the newly created zip file

# Calculate total size before zipping
total_size = 0
for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if d not in exclude_dirs]
    for file in files:
        file_path = os.path.join(root, file)
        if file in exclude_files:
            continue
        total_size += os.path.getsize(file_path)

# Print total size before zipping
print(f"Total size before zipping: {total_size / (1024*1024):.2f} MB")

# Create zip file
with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for file in files:
            file_path = os.path.join(root, file)
            if file in exclude_files:
                continue
            zipf.write(file_path, os.path.relpath(file_path, start='.'))

print(f"Everything zipped into {zip_filename}")
