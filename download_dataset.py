import os
import zipfile
import gdown

# URL from Google Drive share link (converted to gdown format)
GDRIVE_URL = "https://drive.google.com/file/d/1R33Ci-pvCxDC7JqZX9Ns-wr0-NnAIywF/view?usp=sharing"

# Target path
DATASET_DIR = "data"
ZIP_PATH = os.path.join(DATASET_DIR, "dataset.zip")

os.makedirs(DATASET_DIR, exist_ok=True)

# Download the file
print("Downloading dataset...")
gdown.download(GDRIVE_URL, ZIP_PATH, quiet=False)

# Extract it
print("Extracting...")
with zipfile.ZipFile(ZIP_PATH, 'r') as zip_ref:
    zip_ref.extractall(DATASET_DIR)

# Clean up zip
os.remove(ZIP_PATH)

print("Done.")
