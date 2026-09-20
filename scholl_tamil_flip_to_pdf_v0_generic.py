from pathlib import Path
from PIL import Image
import img2pdf
from natsort import natsorted

def convert_with_img2pdf(images, output_pdf_path):
    """Lossless conversion directly embedding original JPG bytes (exact quality)."""
    print(f"Creating {output_pdf_path.name} with img2pdf (lossless)...")
    output_pdf_path.write_bytes(img2pdf.convert([str(p) for p in images]))
    size_mb = output_pdf_path.stat().st_size / (1024 * 1024)
    print(f"Saved: {output_pdf_path.name} ({size_mb:.1f} MB)")

def convert_with_pillow(images, output_pdf_path):
    """Compressed conversion using Pillow (smaller file size, lossy re-encoding)."""
    print(f"Creating {output_pdf_path.name} with Pillow (compressed)...")
    pil_images = []
    try:
        for img_path in images:
            try:
                img = Image.open(img_path)
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")
                pil_images.append(img)
            except Exception as e:
                print(f"Error opening {img_path}: {e}. Skipping.")

        if not pil_images:
            print("No valid images could be opened for Pillow conversion.")
            return

        pil_images[0].save(
            output_pdf_path,
            "PDF",
            resolution=100.0,
            save_all=True,
            append_images=pil_images[1:],
        )
        size_mb = output_pdf_path.stat().st_size / (1024 * 1024)
        print(f"Saved: {output_pdf_path.name} ({size_mb:.1f} MB)")
    finally:
        for img in pil_images:
            img.close()

# Points to the directory where this script resides
root_directory = Path(__file__).parent
directory_prefix = "preschool2/preschool2_text_2019"

for folder in root_directory.glob(f"{directory_prefix}*"):
    if not folder.is_dir():
        continue

    images = natsorted(folder.glob("*.jpg"))
    if not images:
        print(f"No .jpg files found in {folder}")
        continue

    print(f"\nProcessing {folder.name} ({len(images)} pages)...")

    # 1. Lossless PDF using img2pdf (has _img2pdf suffix)
    pdf_img2pdf_path = folder / f"{folder.name}_img2pdf.pdf"
    convert_with_img2pdf(images, pdf_img2pdf_path)

    # 2. Compressed PDF using Pillow
    pdf_pillow_path = folder / f"{folder.name}.pdf"
    convert_with_pillow(images, pdf_pillow_path)
