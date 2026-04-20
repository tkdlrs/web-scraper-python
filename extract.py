from bs4 import BeautifulSoup
# 
def get_heading_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    first_header = soup.find("h1")
    # fall back to h2
    if first_header is None:
        first_header = soup.find("h2")
    # webpage does not have h1 or h2
    if first_header is None:
        return ""
    # 
    return first_header.get_text()
# 
def get_first_paragraph_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    first_paragraph = soup.find_all("p", limit=1)
    # 
    main = soup.find('main')
    first_useful_paragraph = []
    if main: 
        first_useful_paragraph = main.find_all("p", limit=1)
    # 
    if len(first_useful_paragraph) >= 1:
        return first_useful_paragraph[0].get_text()
    # 
    if len(first_paragraph) == 0:
        return ""
    # 
    return first_paragraph[0].get_text()
# 