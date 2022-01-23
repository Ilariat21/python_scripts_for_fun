import requests
import os 
import shutil
from PIL import Image
from fpdf import FPDF
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlparse

def is_valid(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def get_all_images(url):
    soup = bs(requests.get(url).content, "html.parser")
    urls = []
    for img in tqdm(soup.find_all("img"), "Extracting images"):
        img_url = img.attrs.get("src")
        if not img_url:
            continue
        img_url = urljoin(url, img_url)
        try:
            pos = img_url.index("?")
            img_url = img_url[:pos]
        except ValueError:
            pass
        if is_valid(img_url):
            urls.append(img_url)
    return urls

def download(url, pathname, name):
    if not os.path.isdir(pathname):
        os.makedirs(pathname)
    response = requests.get(url, stream=True)
    file_size = int(response.headers.get("Content-Length", 0))
    filename = os.path.join(pathname, name + ".jpg")
    progress = tqdm(response.iter_content(1024), f"Downloading {filename}", total=file_size, unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "wb") as f:
        for data in progress.iterable:
            f.write(data)
            progress.update(len(data))
    return filename

def get_imgs(url, path):
    image_list = []
    imgs = get_all_images(url)
    i = 0
    for img in imgs:
        filename = download(img, path, "page_" + str(i))
        image_list.append(filename)
        i += 1
    return image_list

def create_list(imgs):
    img_list = []
    for i in range(1, len(imgs)-1):
        img = Image.open(imgs[i])
        img_list.append(img)
    return img_list

def main(url, pdf_filename):
    path = "temporary_folder_for_manga"
    imgs = get_imgs(url, path)
    pdf = FPDF()
    im1 = Image.open(imgs[0])
    img_list = create_list(imgs)
    im1.save(pdf_filename + ".pdf", "PDF", resolution=100.0, save_all=True, append_images=img_list)
    shutil.rmtree(path)
    print("Done")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="This script downloads all images from a web page and creates a pdf file from them")
    parser.add_argument("url", help="The URL of the web page you want to download images")
    parser.add_argument("-n", "--name", help="The name of the pdf file, default is the domain of URL passed")
    
    args = parser.parse_args()
    url = args.url
    pdf_filename = args.name

    if not pdf_filename:
        # if path isn't specified, use the domain name of that url as the folder name
        pdf_filename = urlparse(url).netloc
    
    main(url, pdf_filename)
