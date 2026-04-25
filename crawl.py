from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import  requests 
# 
def normalize_url(url):
    parsed_url = urlparse(url)
    full_path = f"{parsed_url.netloc}{parsed_url.path}"
    full_path = full_path.rstrip("/") 
    return full_path.lower()
# 
def get_heading_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    h_tag = soup.find("h1") or soup.find("h2")
    return h_tag.get_text(strip=True) if h_tag else ""
# 
def get_first_paragraph_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    # 
    main_section = soup.find('main')
    if main_section:
        first_p = main_section.find("p")
    else:
        first_p = soup.find("p")
    # 
    return first_p.get_text(strip=True) if first_p else ""
# 
def get_urls_from_html(html, base_url):
    urls = []
    soup = BeautifulSoup(html, 'html.parser')
    anchors = soup.find_all("a")
    # 
    for a in anchors:
        if href := a.get("href"):
            try:
                absolute_url = urljoin(base_url, href)
                urls.append(absolute_url)
            except Exception as e:
                print(f"{str(e)}: {href}")
    # 
    return urls
# 
def get_images_from_html(html, base_url):
    image_urls = []
    soup = BeautifulSoup(html, 'html.parser')
    images = soup.find_all("img")
    # 
    for img in images:
        if src := img.get("src"):
            try:
                absolute_url = urljoin(base_url, src)
                image_urls.append(absolute_url)
            except Exception as e:
                print(f"{str(e)}: {src}")
    # 
    return image_urls
# 
def extract_page_data(html, page_url):
    header = get_heading_from_html(html) 
    lead = get_first_paragraph_from_html(html)
    links = get_urls_from_html(html, page_url)
    images = get_images_from_html(html, page_url)
    # 
    return {
        "url": page_url,
        "heading": header,
        "first_paragraph": lead,
        "outgoing_links": links,
        "image_urls":  images
    }
# 
def crawl_page(base_url, current_url=None, page_data=None):
    if current_url is None:
        current_url = base_url
    # 
    if page_data is None:
        page_data = {}
    # 
    base_url_obj = urlparse(base_url)
    current_url_obj = urlparse(current_url)
    if current_url_obj.netloc != base_url_obj.netloc:
        return page_data
    # 
    normalized_url = normalize_url(current_url)
    if normalized_url in page_data:
        return page_data
    # 
    print(f"crawling {current_url}")
    html = safe_get_html(current_url)
    if html is None:
        return page_data
    # 
    page_info = extract_page_data(html, current_url)
    page_data[normalized_url] = page_info
    # recursive part 
    next_urls = get_urls_from_html(html, base_url)
    for next_url in next_urls:
        page_data = crawl_page(base_url, next_url, page_data)
    # 
    return page_data
# 
def get_html(url):
    try:
        response = requests.get(url, headers={"User-Agent": "BootCrawler/1.0"})
    except Exception as e:
        raise Exception(f"network error while fething {url}: {e}")
    # 
    if response.status_code > 399:
        raise Exception(f"got HTTP error: {response.status_code} {response.reason}")
    # 
    content_type = response.headers.get("content-type")
    if "text/html" not in content_type: 
        raise Exception(f"got non-HTML response:  {content_type}")
    # 
    return response.text
# 
def safe_get_html(url):
    try:
        return get_html(url)
    except Exception as e:
        print(f"{e}")
        return None