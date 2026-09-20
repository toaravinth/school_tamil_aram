import os
import re
import requests
from collections import defaultdict
import urllib.parse

def find_urls_in_code(directory="."):
    urls = set()
    url_pattern = re.compile(r'https?://[^\s\"\'\\]+')
    for root, dirs, files in os.walk(directory):
        if '.git' in root or '.agents' in root:
            continue
        for file in files:
            if file.endswith('.py'):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    for line in f:
                        matches = url_pattern.findall(line)
                        for match in matches:
                            urls.add(match)
    return urls

def test_url(url):
    print(f"Testing {url} ... ", end="")
    try:
        response = requests.head(url, allow_redirects=True, timeout=10)
        if response.status_code == 200:
            print("OK")
            return True
        elif response.status_code == 405:
            # Sometimes HEAD is not allowed, try GET
            response = requests.get(url, allow_redirects=True, timeout=10)
            if response.status_code == 200:
                print("OK")
                return True
        print(f"Failed ({response.status_code})")
        return False
    except requests.RequestException as e:
        print(f"Error: {e}")
        return False

def check_and_get_valid_urls(base_urls):
    valid_urls = set()
    suffixes_to_try = [
        "/index.html",
        "/mobile/index.html",
        "/mobile/index1.html",
        ""
    ]
    for base in base_urls:
        # Some URLs in code already contain suffix or are just partial.
        # Let's clean the base URL if it contains suffix already
        base = base.split('/index.html')[0]
        base = base.split('/mobile/index.html')[0]
        base = base.split('/mobile/index1.html')[0]
        
        found = False
        for suffix in suffixes_to_try:
            test = base + suffix
            if test_url(test):
                valid_urls.add(test)
                found = True
                break
        if not found:
            print(f"WARNING: Could not find a valid page for {base}")
    return valid_urls

def group_urls_by_grade(urls):
    groups = defaultdict(list)
    for url in urls:
        # Extract grade from URL, e.g. .../CTA%20Text%20book/Grade%201/...
        match = re.search(r'CTA(?:%20|\s)Text(?:%20|\s)book/([^/]+)/', url, re.IGNORECASE)
        if match:
            grade = urllib.parse.unquote(match.group(1)).strip()
            groups[grade].append(url)
        else:
            groups['Other'].append(url)
            
    for grade in groups:
        groups[grade] = sorted(list(set(groups[grade])))
    return groups

def update_readme(groups, readme_path="README.md"):
    with open(readme_path, 'w', encoding='utf-8') as f:
        # define a sorted order for known grades
        order = ['Preschool 1', 'Preschool 2', 'Kindergarten', 'Grade 1', 'Grade 2', 'Grade 3', 'Grade 4', 'Grade 5', 'Grade 6', 'Grade 7', 'Grade 8']
        
        # Sort grades based on the defined order, or alphabetically for unknown ones
        def sort_key(k):
            try:
                return order.index(k)
            except ValueError:
                return len(order)
                
        for grade in sorted(groups.keys(), key=sort_key):
            f.write(f"# {grade}\n")
            for url in groups[grade]:
                f.write(f"{url}\n")
            f.write("\n")
    print("README.md updated successfully.")

def main():
    print("Finding URLs in Python files...")
    code_urls = find_urls_in_code()
    
    # Also parse current README to ensure we don't lose any existing URLs that might not be in the python files
    print("Finding URLs in current README.md...")
    try:
        with open('README.md', 'r', encoding='utf-8') as f:
            for line in f:
                matches = re.findall(r'https?://[^\s\"\'\\]+', line)
                for match in matches:
                    code_urls.add(match)
    except FileNotFoundError:
        print("README.md not found, will create a new one.")
        
    print(f"Found {len(code_urls)} unique URLs/base-paths. Testing them...")
    valid_urls = check_and_get_valid_urls(code_urls)
    
    print("Grouping URLs...")
    grouped = group_urls_by_grade(valid_urls)
    
    print("Updating README.md...")
    update_readme(grouped)

if __name__ == "__main__":
    main()
