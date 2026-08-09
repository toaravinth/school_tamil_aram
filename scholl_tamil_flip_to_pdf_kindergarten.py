import os
import fnmatch
from PIL import Image
from reportlab.pdfgen import canvas
from urllib.parse import urlparse, urlunparse

def convert_images_to_pdf(input_images, output_pdf_path):
    input_images.sort()
    # Create a PDF file
    with open(output_pdf_path, 'wb') as pdf_file:
        # Iterate over the list of input images
        for input_image_path in input_images:
            # Open each JPG image
            img = Image.open(input_image_path)
            print("img.width="+str(img.width))

            # Create a PDF canvas for each image
            pdf_canvas = canvas.Canvas(pdf_file, pagesize=img.size)
            print("pdf_canvas="+str(pdf_canvas))

            # Draw the JPG image on the PDF canvas
            pdf_canvas.drawImage(input_image_path, 0, 0, width=img.width, height=img.height)

            # Save the PDF canvas for the current image
            pdf_canvas.showPage()
            print("pdf_canvas.showPage()")

    print(f'Conversion complete. PDF saved at {output_pdf_path}')

def find_directories_with_prefix(root_dir, prefix):
    matching_directories = []

    for dirpath, dirnames, filenames in os.walk(root_dir):
        for dirname in fnmatch.filter(dirnames, prefix + '*'):
            matching_directories.append(os.path.join(dirpath, dirname))

    return matching_directories

def list_files_with_extension(directory, extension):
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(extension):
                file_path = os.path.join(root, file)
                file_list.append(file_path)
    return file_list

# Specify the root directory and the prefix
root_directory = '/Users/aravinth/Library/CloudStorage/GoogleDrive-toaravinth@gmail.com/My Drive/custom/projects/github/toaravinth/general/aram_tamil_school/'
directory_prefix = 'grade1_txt_2023'

# Get a list of directories with the specified prefix
matching_directories = find_directories_with_prefix(root_directory, directory_prefix)

# Print the matching directories
for directory in matching_directories:
    file_extension = '.jpg'
    input_images = list_files_with_extension(directory, file_extension)

    parsed_url = urlparse(directory)
    path_parts = parsed_url.path.split('/')
    output_pdf_path = directory + "/" + str(path_parts[len(path_parts) - 1] + ".pdf")

    convert_images_to_pdf(input_images, output_pdf_path)
