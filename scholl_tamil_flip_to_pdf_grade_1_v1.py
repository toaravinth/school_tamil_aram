import os
import fnmatch
import natsort
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader # More robust way to handle images
from reportlab.lib.pagesizes import letter # Or use image size

def convert_images_to_pdf_reportlab(input_images, output_pdf_path):
    if not input_images:
        print(f"No images found to convert for {output_pdf_path}")
        return

    sorted_images = natsort.natsorted(input_images)
    # input_images.sort() # Sort images alphabetically/numerically

    try:
        # --- Canvas Initialization (Outside the loop) ---
        # Option 1: Use the size of the first image for all pages
        first_img = Image.open(sorted_images[0])
        page_width, page_height = first_img.size
        # Ensure PIL object is closed if you don't need it anymore
        # first_img.close() # Close if not needed below, but ImageReader handles it

        # Option 2: Use a standard page size (like letter or A4)
        # page_width, page_height = letter # Example: from reportlab.lib.pagesizes import letter

        c = canvas.Canvas(output_pdf_path, pagesize=(page_width, page_height))

        print(f"Creating PDF: {output_pdf_path} with page size: {page_width}x{page_height}")

        # --- Loop Through Images ---
        for image_path in sorted_images:
            try:
                # Use ImageReader for better handling
                img_reader = ImageReader(image_path)
                # Get actual image dimensions
                img_width, img_height = img_reader.getSize()

                # --- Draw Image ---
                # Center image on page (optional) or scale to fit
                # For simplicity, draw at 0,0 with its own size
                # Note: If image is larger than page_size, it will be clipped.
                # You might want scaling logic here.
                c.setPageSize((img_width, img_height)) # Set page size for *this* page to match image
                c.drawImage(img_reader, 0, 0, width=img_width, height=img_height)

                # --- Finish Page ---
                c.showPage()
                print(f"Added {os.path.basename(image_path)} to PDF.")

            except Exception as e:
                print(f"Error processing image {image_path}: {e}")
                # Decide if you want to skip the image or stop the PDF creation

        # --- Save the PDF (After the loop) ---
        c.save()
        print(f'Conversion complete. PDF saved at {output_pdf_path}')

    except Exception as e:
        print(f"Failed to create PDF {output_pdf_path}: {e}")


def find_directories_with_prefix(root_dir, prefix):
    matching_directories = []
    if not os.path.isdir(root_dir):
        print(f"Error: Root directory '{root_dir}' not found.")
        return []
    for entry in os.scandir(root_dir):
        if entry.is_dir() and entry.name.startswith(prefix):
             matching_directories.append(entry.path)
        # If you need to search recursively:
        # for dirpath, dirnames, filenames in os.walk(root_dir):
        #     for dirname in fnmatch.filter(dirnames, prefix + '*'):
        #         matching_directories.append(os.path.join(dirpath, dirname))
        #     break # Only search top-level if using os.walk like this
    return matching_directories


def list_files_with_extension(directory, extension):
    file_list = []
    try:
        for root, dirs, files in os.walk(directory):
            for file in files:
                # Ensure case-insensitivity for extensions if needed
                if file.lower().endswith(extension.lower()):
                    file_path = os.path.join(root, file)
                    file_list.append(file_path)
    except Exception as e:
        print(f"Error listing files in {directory}: {e}")
    return file_list

# --- Main Execution ---
# Specify the root directory and the prefix
# Use raw string (r"...") or forward slashes for paths, especially on Windows
root_directory = r'/Users/aravinth/Library/CloudStorage/GoogleDrive-toaravinth@gmail.com/My Drive/custom/projects/github/toaravinth/general/aram_tamil_school/'
directory_prefix = 'grade1_txt_2023'
file_extension = '.jpg' # Or '.jpeg' or handle both

# Get a list of directories with the specified prefix (adjust find_directories_with_prefix if recursive needed)
matching_directories = find_directories_with_prefix(root_directory, directory_prefix)

if not matching_directories:
    print(f"No directories found starting with '{directory_prefix}' in '{root_directory}'")
else:
    # Process each matching directory
    for directory in matching_directories:
        print(f"\nProcessing directory: {directory}")
        input_images = list_files_with_extension(directory, file_extension)

        if input_images:
            # --- Simplified Output Path ---
            # Get the base name of the directory (e.g., 'grade1_txt_2023_folder')
            dir_name = os.path.basename(directory)
            # Create the output PDF name in the same directory
            output_pdf_path = os.path.join(directory, f"{dir_name}.pdf")

            # --- Call the Conversion Function ---
            convert_images_to_pdf_reportlab(input_images, output_pdf_path)
        else:
            print(f"No '{file_extension}' files found in {directory}")