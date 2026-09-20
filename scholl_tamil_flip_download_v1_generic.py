import os
import re
import urllib.parse
import requests


# grade Preschool 1
# book_urls=[
#     "https://www.catamilacademy.org/cta/CTA%20Text%20book/Preschool%201/Preschool1_hwb_2019",
#     "https://www.catamilacademy.org/cta/CTA%20Text%20book/Preschool%201/Preschool1%20_text_2019"
# ]

# grade Preschool 2
book_urls=[
    "https://www.catamilacademy.org/cta/CTA%20Text%20book/Preschool%202/preschool2_exe_2019/mobile/index1.html",
    "https://www.catamilacademy.org/cta/CTA%20Text%20book/Preschool%202/preschool2_text%20_2019/mobile/index1.html"
]

# grade 1
# book_urls=[
#   "https://www.catamilacademy.org/cta/CTA%20Text%20book/Grade%201/grade1_txt_2023"
# ]

# grade 2
# book_urls=[
#   "https://www.catamilacademy.org/cta/CTA%20Text%20book/Grade%202/grade2_hwb_2023",
#   "https://www.catamilacademy.org/cta/CTA%20Text%20book/Grade%202/grade2_txt_2023",
#   "https://www.catamilacademy.org/cta/CTA%20Text%20book/Grade%202/grade2_exe_2023"
# ]

# grade 3
# book_urls=[
  # "https://www.catamilacademy.org/cta/CTA%20Text%20book/Grade%203/grade3_hwb_2023",
  # "https://www.catamilacademy.org/cta/CTA%20Text%20book/Grade%203/grade3_exe_text_2023_part1",
  # "https://www.catamilacademy.org/cta/CTA%20Text%20book/Grade%203/grade3_exe_text_2023_part2"
# ]

def normalize_book_url(url):
    """
    Strips web viewer endings (/mobile/index.html, /index.html, etc.)
    and returns: (base_book_url, grade_name, book_name)
    """
    # Remove query params or fragments
    parsed = urllib.parse.urlparse(url)
    clean_path = parsed.path.rstrip('/')
    
    # Strip known viewer file endings
    clean_path = re.sub(r'/(mobile/)?index\d*\.html?$', '', clean_path, flags=re.IGNORECASE)
    
    # Base URL for downloading assets
    base_url = urllib.parse.urlunparse((parsed.scheme, parsed.netloc, clean_path, '', '', ''))
    
    # Extract path parts
    path_segments = [urllib.parse.unquote(p) for p in clean_path.split('/') if p]
    book_name = path_segments[-1] if path_segments else "unknown_book"
    
    # Try to extract grade from URL structure (e.g. 'CTA Text book/<Grade>/<Book>')
    grade_name = None
    for i, seg in enumerate(path_segments):
        if "cta text book" in seg.lower() and i + 1 < len(path_segments):
            grade_name = path_segments[i + 1]
            break
            
    # Fallback: derive grade from book name (e.g. "grade2" from "grade2_exe_2023")
    if not grade_name or grade_name == book_name:
        grade_name = book_name.split('_')[0]
        
    # Standardize grade folder name (e.g., "Grade 1" -> "grade1" or keep as desired)
    grade_dir = grade_name.replace(" ", "").lower()
    
    return base_url, grade_dir, book_name

def download_book(book_url, session):
    base_url, grade_dir, book_name = normalize_book_url(book_url)
    target_dir = os.path.join(grade_dir, book_name)
    
    # Automatically create all nested directories
    os.makedirs(target_dir, exist_ok=True)
    print(f"\n==========================================")
    print(f"Processing: {book_name}")
    print(f"Target Directory: {target_dir}")
    print(f"Base Asset URL: {base_url}")
    print(f"==========================================")

    page_num = 1
    while True:
        file_name = f"{page_num}.jpg"
        image_url = f"{base_url}/files/mobile/{file_name}"
        save_path = os.path.join(target_dir, file_name)

        if os.path.exists(save_path) and os.path.getsize(save_path) > 0:
            print(f"Page {page_num} already exists, skipping...")
            page_num += 1
            continue

        resp = session.get(image_url)
        if resp.status_code == 200:
            with open(save_path, 'wb') as f:
                f.write(resp.content)
            print(f"Downloaded: {file_name} -> {save_path}")
            page_num += 1
        elif resp.status_code == 404:
            print(f"Completed! Total pages downloaded: {page_num - 1}")
            break
        else:
            print(f"Received status code {resp.status_code} on page {page_num}. Stopping.")
            break

def main():
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    }
    with requests.Session() as session:
        session.headers.update(headers)
        for url in book_urls:
            download_book(url, session)

if __name__ == "__main__":
    main()
