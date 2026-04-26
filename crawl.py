from urllib.parse import urlparse, urljoin
import asyncio 
from bs4 import BeautifulSoup
import aiohttp 

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

# 
class AsyncCrawler:
    def __init__(self, base_url):
        self.base_url = base_url
        self.base_domain = urlparse(base_url).netloc 
        self.page_data = {} 
        self.lock = asyncio.Lock()
        self.max_concurrency = 3
        self.semaphore = asyncio.Semaphore(self.max_concurrency)
        self.session = None 
    # 
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self 
    # 
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()
    # 
    async def add_page_visit(self, normalized_url):
        async with self.lock:
            if normalized_url in self.page_data:
                return False
            else:
                return True       
    #
    async def get_html(self, url):
        try:
            async with self.session.get(
                url, headers={"User-Agent": "BootCrawler/1.0"}
            ) as response:
                if response.status > 399:
                    print(f"Error: HTTP {response.status} for {url}")
                    return None
                # 
                content_type = response.headers.get("content-type", "")
                if "text/html" not in content_type: 
                    print(f"Error: Non-HTML content {content_type} for {url}")
                    return None
                # 
                return await response.text()
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None
    # 
    async def crawl_page(self, current_url):
        current_url_obj = urlparse(current_url)
        if current_url_obj.netloc != self.base_domain:
            return
        # 
        normalized_url = normalize_url(current_url)
        # 
        is_new = await self.add_page_visit(normalized_url)
        if not is_new:
            return 
        # 
        async with self.semaphore:
            print(
                f"crawling {current_url} (Active: {self.max_concurrency - self.semaphore._value})"
            )
            html = await self.get_html(current_url)
            if html is None:
                return 
            # 
            page_info = extract_page_data(html, current_url)
            async with self.lock:
                self.page_data[normalized_url] = page_info
            #
            next_urls = get_urls_from_html(html, self.base_url)
        # 
        tasks = []
        for next_url in next_urls:
           tasks.append(asyncio.create_task(self.crawl_page(next_url)))
        # 
        if tasks:
            await asyncio.gather(*tasks)
        # 
    # 
    async def crawl(self):
        await self.crawl_page(self.base_url)
        return self.page_data
    #  
# 
async def crawl_site_async(base_url):
    async with AsyncCrawler(base_url) as crawler:
        return await crawler.crawl()