import requests, os
from urllib.parse import urlparse, urlunparse

book_urls=[
    "https://www.catamilacademy.org/cta/CTA%20Text%20book/Preschool%201/Preschool1_hwb_2019",
    "https://www.catamilacademy.org/cta/CTA%20Text%20book/Preschool%201/Preschool1%20_text_2019"
]

# book_urls=[
#   
# ]

suffix_index_page="/mobile/index.html"
suffix_image_path="/files/mobile/"
suffix_ext=".jpg"
n = 1;

def create_directory(directory_path):
  if not os.path.exists(directory_path):
    os.makedirs(directory_path)
    print(f"Directory created: {directory_path}")
  else:
    print(f"Directory already exists: {directory_path}")

def download_image(url, save_path):
  response = requests.get(url)
  if response.status_code == 200:
    with open(save_path, 'wb') as file:
      file.write(response.content)
    print(f"Image downloaded successfully and saved at: {save_path}")
  else:
    print(f"Failed to download image. Status code: {response.status_code}")

for book_url in book_urls:
  parsed_url = urlparse(book_url)
  path_parts = parsed_url.path.split('/')
  trimmed_path = path_parts[len(path_parts)-1]
  
  # Extract the grade directory from trimmed_path (e.g., "grade2" from "grade2_exe_2023")
  grade_dir = trimmed_path.split('_')[0]
  
  # Create the full path: grade2/grade2_exe_2023
  book_dir = f"{grade_dir}/{trimmed_path}"
  
  print("trimmed_path="+str(trimmed_path))
  create_directory(book_dir)
  print("main_page=" + book_url + suffix_index_page)
  n=1
  while True:
    file_name=str(n) + suffix_ext
    image_url=book_url + suffix_image_path +file_name
    print("image_url=" + image_url)
    resp = requests.get(image_url)
    if resp.status_code == 200:
      download_image(image_url, book_dir+"/"+file_name)
    else:
      print('Done!')
      break
    n=n+1;
    # if(n>1):
    #   break
