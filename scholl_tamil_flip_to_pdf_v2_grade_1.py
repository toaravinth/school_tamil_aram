import os
import fnmatch
import natsort
from PIL import Image

def convert_images_to_pdf_pillow(input_images, output_pdf_path):
    if not input_images:
        print(f"No images found to convert for {output_pdf_path}")
        return
    sorted_images = natsort.natsorted(input_images)
    # input_images.sort() # Sort images alphabetically/numerically

    pil_images = []
    try:
        # Open all images first
        for image_path in sorted_images:
            try:
                img = Image.open(image_path)
                # Convert RGBA (like PNGs with transparency) or P (paletted) to RGB
                if img.mode == 'RGBA' or img.mode == 'P':
                    img = img.convert('RGB')
                pil_images.append(img)
                print(f"Opened {os.path.basename(image_path)}")
            except Exception as e:
                print(f"Error opening image {image_path}: {e}. Skipping.")
                # Clean up already opened images if one fails? Optional.

        if not pil_images:
             print("No valid images could be opened.")
             return

        # --- Save to PDF ---
        # The first image in the list is used to initialize the PDF.
        # `append_images` adds the rest.
        print(f"Creating PDF: {output_pdf_path}")
        pil_images[0].save(
            output_pdf_path,
            "PDF",
            resolution=100.0, # Adjust DPI if needed
            save_all=True,     # Required to save multiple images
            append_images=pil_images[1:] # Append the rest of the images
        )
        print(f'Conversion complete. PDF saved at {output_pdf_path}')

    except Exception as e:
        print(f"Failed to create PDF {output_pdf_path}: {e}")

    finally:
        # --- Important: Close images ---
        for img in pil_images:
            img.close()


# --- Helper functions (same as Version 1) ---

def find_directories_with_prefix(root_dir, prefix):
    matching_directories = []
    if not os.path.isdir(root_dir):
        print(f"Error: Root directory '{root_dir}' not found.")
        return []
    for entry in os.scandir(root_dir):
        if entry.is_dir() and entry.name.startswith(prefix):
             matching_directories.append(entry.path)
    # Add os.walk logic here if recursive search needed (see version 1)
    return matching_directories


def list_files_with_extension(directory, extension):
    file_list = []
    try:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.lower().endswith(extension.lower()):
                    file_path = os.path.join(root, file)
                    file_list.append(file_path)
    except Exception as e:
        print(f"Error listing files in {directory}: {e}")
    return file_list

# --- Main Execution (same as Version 1, but calls the Pillow function) ---
root_directory = r'/Users/aravinth/Library/CloudStorage/GoogleDrive-toaravinth@gmail.com/My Drive/custom/projects/github/toaravinth/school_tamil_aram/grade3'
directory_prefix = 'grade3_hwb_2023'
file_extension = '.jpg'

matching_directories = find_directories_with_prefix(root_directory, directory_prefix)

if not matching_directories:
    print(f"No directories found starting with '{directory_prefix}' in '{root_directory}'")
else:
    for directory in matching_directories:
        print(f"\nProcessing directory: {directory}")
        input_images = list_files_with_extension(directory, file_extension)

        if input_images:
            dir_name = os.path.basename(directory)
            output_pdf_path = os.path.join(directory, f"{dir_name}.pdf")
            # --- Call the Pillow Conversion Function ---
            convert_images_to_pdf_pillow(input_images, output_pdf_path)
        else:
            print(f"No '{file_extension}' files found in {directory}")