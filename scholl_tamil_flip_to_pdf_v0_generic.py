from pathlib import Path
import img2pdf
from natsort import natsorted

# Points to the directory where this script resides
root_directory = Path(__file__).parent
directory_prefix = "grade3/grade3_exe_text_2023_part1"

for folder in root_directory.glob(f"{directory_prefix}*"):
    if not folder.is_dir():
        continue
    
    # Use rglob if images might be in nested subfolders, otherwise glob is fine
    images = natsorted(folder.glob("*.jpg"))
    if not images:
        continue

    pdf_path = folder / f"{folder.name}.pdf"
    print(f"Creating {pdf_path} ({len(images)} pages)...")
    pdf_path.write_bytes(img2pdf.convert([str(p) for p in images]))
    print(f"Saved: {pdf_path}")
