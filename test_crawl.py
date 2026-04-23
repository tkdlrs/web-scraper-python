import unittest
from crawl import (
    normalize_url, 
    get_heading_from_html, 
    get_first_paragraph_from_html, 
    get_urls_from_html, 
    get_images_from_html, 
    extract_page_data,
)

# 
class Case:
    def __init__(self, i, e):
        self.i = i
        self.e = e


class TestCrawl(unittest.TestCase):
    # Boot.dev 
    def test_get_urls_from_html_absolute(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="https://crawler-test.com"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_relative(self):
        input_url = "https://crawler-test.com"
        input_body = (
            '<html><body><a href="/path/one"><span>Boot.dev</span></a></body></html>'
        )
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/path/one"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_both(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="/path/one"><span>Boot.dev</span></a><a href="https://other.com/path/one"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/path/one", "https://other.com/path/one"]
        self.assertEqual(actual, expected)
    #  mine
    def test_normalize_url(self):
        input_url = "https://www.boot.dev/blog/path"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)
    #
    def test_normalize_url_2(self):
        # 
        test_cases = []
        test_cases.append(Case("https://www.boot.dev/blog/path", "www.boot.dev/blog/path"))
        test_cases.append(Case("https://www.boot.dev/blog/path/", "www.boot.dev/blog/path"))
        test_cases.append(Case("http://www.boot.dev/blog/path", "www.boot.dev/blog/path"))
        test_cases.append(Case("http://www.boot.dev/blog/path/", "www.boot.dev/blog/path"))
        # 
        for case in test_cases:
            a = normalize_url(case.i)
            self.assertEqual(a, case.e)      
    # 
    def test_normalize_url_protocol(self):
        input_url = "https://crawler-test.com/path"
        actual = normalize_url(input_url)
        expected = "crawler-test.com/path"
        self.assertEqual(actual, expected)
    # 
    def test_normalize_url_slash(self):
        input_url = "https://crawler-test.com/path/"
        actual = normalize_url(input_url)
        expected = "crawler-test.com/path"
        self.assertEqual(actual, expected)
    # 
    def test_normalize_url_capitals(self):
        input_url = "https://CRAWLER-TEST.com/path"
        actual = normalize_url(input_url)
        expected = "crawler-test.com/path"
        self.assertEqual(actual, expected)
    # 
    def test_normalize_url_http(self):
        input_url = "http://CRAWLER-TEST.com/path"
        actual = normalize_url(input_url)
        expected = "crawler-test.com/path"
        self.assertEqual(actual, expected)
    #     

# 
class TestExtract(unittest.TestCase):
    """
    Start Header tests
    """
    # From Boot.dev
    def test_get_heading_form_html_basic(self):
        input_body = '<html><body><h1>Test Title</h1></body></html>'
        actual = get_heading_from_html(input_body)
        expected  = "Test Title"
        self.assertEqual(actual, expected)
    def test_get_heading_from_html_basic(self):
        input_body = "<html><body><h1>Test Title</h1></body></html>"
        actual = get_heading_from_html(input_body)
        expected = "Test Title"
        self.assertEqual(actual, expected)

    def test_get_heading_from_html_h2_fallback(self):
        input_body = "<html><body><h2>Fallback Title</h2></body></html>"
        actual = get_heading_from_html(input_body)
        expected = "Fallback Title"
        self.assertEqual(actual, expected)

    def test_get_heading_from_html_with_whitespace(self):
        input_body = "<html><body><h1>   Whitespace Title   </h1></body></html>"
        actual = get_heading_from_html(input_body)
        expected = "Whitespace Title"
        self.assertEqual(actual, expected)
     
    # MINE
    def test_header(self):
        markup = """<h1>This is noise</h1>"""
        actual = get_heading_from_html(markup)
        expected = "This is noise"
        self.assertEqual(actual, expected)
    # 
    def test_header_more_boiler_plate(self):
        markup = """<html>
        <body>
            <h1>Welcome to Boot.dev</h1>
            <main>
                <p>Learn to code by building real projects.</p>
                <p>This is the second paragraph.</p>
            </main>
        </body>
    </html>"""
        actual = get_heading_from_html(markup)
        expected = "Welcome to Boot.dev" 
        self.assertEqual(actual, expected)
    # 
    def test_fallback_to_h2(self):
        markup = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Document</title>
        </head>
        <body>
            <p>This is noise</p>
            <h2>This is the closest thing to an actual header this page has.</h2>
            <p>It isn't accessible or using header tags in a semantically correct manner.</p> 
        </body>
        </html>"""
        actual = get_heading_from_html(markup)
        expected = "This is the closest thing to an actual header this page has."
        self.assertEqual(actual, expected)
    # 


    """
    Start Paragraph tests
    """ 
    # From Boot.dev
    def test_get_first_paragraph_from_html_main_priority(self):
        input_body = '''<html><body>
        <p>Outside paragraph.</p>
        <main>
            <p>Main paragraph.</p>
        </main>
        </body></html>'''
        actual = get_first_paragraph_from_html(input_body)
        expected = "Main paragraph."
        self.assertEqual(actual, expected)
    def test_get_first_paragraph_from_html_basic(self):
        input_body = "<html><body><p>This is the first paragraph.</p></body></html>"
        actual = get_first_paragraph_from_html(input_body)
        expected = "This is the first paragraph."
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_main_priority(self):
        input_body = """<html><body>
            <p>Outside paragraph.</p>
            <main>
                <p>Main paragraph.</p>
            </main>
        </body></html>"""
        actual = get_first_paragraph_from_html(input_body)
        expected = "Main paragraph."
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_no_paragraph(self):
        input_body = "<html><body><h1>No paragraphs here</h1></body></html>"
        actual = get_first_paragraph_from_html(input_body)
        expected = ""
        self.assertEqual(actual, expected)
    # MINE
    def test_paragraph(self):
        markup ="""<p>This is noise</p>"""
        actual = get_first_paragraph_from_html(markup)
        expected = "This is noise"
        self.assertEqual(actual, expected)
    # 
    def test_paragaph_more_boiler_plate(self):
        markup = """<html>
        <body>
            <h1>Welcome to Boot.dev</h1>
            <main>
                <p>Learn to code by building real projects.</p>
                <p>This is the second paragraph.</p>
            </main>
        </body>
    </html>"""
        actual = get_first_paragraph_from_html(markup)
        expected = "Learn to code by building real projects." 
        self.assertEqual(actual, expected)
    # 
    def test_no_paragraphs_found(self):
        markup = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Document</title>
        </head>
        <body>
            <h1>Header</h1>
            <span>This is noise</span>
            <span>It isn't accessible or using header tags in a semantically correct manner.</span> 
        </body>
        </html>"""
        actual = get_first_paragraph_from_html(markup)
        expected = ""
        self.assertEqual(actual, expected)
    # 
    """
    Links
    """
    # From Boot.dev
    def test_get_urls_from_html_absolute(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="https://crawler-test.com"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com"]
        self.assertEqual(actual, expected)
    
    def test_get_urls_from_html_absolute(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="https://crawler-test.com"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_relative(self):
        input_url = "https://crawler-test.com"
        input_body = (
            '<html><body><a href="/path/one"><span>Boot.dev</span></a></body></html>'
        )
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/path/one"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_both(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="/path/one"><span>Boot.dev</span></a><a href="https://other.com/path/one"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/path/one", "https://other.com/path/one"]
        self.assertEqual(actual, expected)

    # Mine
    def test_get_url_from_html_relative(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="/"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/"]
        self.assertEqual(actual, expected)
    # 
    def test_get_urls_from_html_absolute_and_relative(self):
        input_url = "https://crawler-test.com"
        input_body = '''
        <html>
            <body>
                <p><a href="/"><span>crawler test</span></a></p>
                <p><a href="https://boot.dev/"><span>Boot dev homepage</span></a></p>
                <p><a href="https://google.com/">Google</a></p>
            </body>
        </html>'''
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/", "https://boot.dev/", "https://google.com/"]
        self.assertEqual(actual, expected)
    #  
    """
    Images
    """
    # From Boot.dev
    def test_get_images_from_html_relative(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="/logo.png" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/logo.png"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_absolute(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="https://crawler-test.com/logo.png" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/logo.png"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_relative(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="/logo.png" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/logo.png"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_multiple(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="/logo.png" alt="Logo"><img src="https://cdn.boot.dev/banner.jpg"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = [
            "https://crawler-test.com/logo.png",
            "https://cdn.boot.dev/banner.jpg",
        ]
        self.assertEqual(actual, expected)
    # Mine
    def test_get_image_from_html_absolute(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><img src="https://crawler-test.com/images/crawler.jpg" alt="crawler"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/images/crawler.jpg"]
        self.assertEqual(actual, expected)
    # 
    def test_get_images_from_html_missing_src(self):
        input_url = "https://crawler-test.com"
        input_body = '''
        <html>
            <body>
                <div><img src="/images/logo.jpg" ></div>
                <p><img  alt="missing a src"></p>
                <p><a href="https://google.com/">Google</a></p>
            </body>
        </html>'''
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/images/logo.jpg"]
        self.assertEqual(actual, expected)
    """
    Whole page data
    """
    # Boot.dev
    def test_extract_page_data_basic(self):
        input_url = "https://crawler-test.com"
        input_body = '''<html><body>
        <h1>Test Title</h1>
        <p>This is the first paragraph.</p>
        <a href="/link1">Link 1</a>
        <img src="/image1.jpg" alt="Image 1">
        </body></html>'''
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "Test Title",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": ["https://crawler-test.com/link1"],
            "image_urls": ["https://crawler-test.com/image1.jpg"]
        }
        self.assertEqual(actual, expected)
    # 
    def test_extract_page_data_main_section(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
            <nav><p>Navigation paragraph</p></nav>
            <main>
                <h1>Main Title</h1>
                <p>Main paragraph content.</p>
            </main>
        </body></html>"""
        actual = extract_page_data(input_body, input_url)
        self.assertEqual(actual["heading"], "Main Title")
        self.assertEqual(actual["first_paragraph"], "Main paragraph content.")
    # 
    def test_extract_page_data_missing_elements(self):
        input_url = "https://crawler-test.com"
        input_body = "<html><body><div>No h1, p, links, or images</div></body></html>"
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "",
            "first_paragraph": "",
            "outgoing_links": [],
            "image_urls": [],
        }
        self.assertEqual(actual, expected)
    # Mine
    def test_extract_page_data_missing_header(self):
        input_url = "https://crawler-test.com"
        input_body = '''<html><body>

        <p>This is the first paragraph.</p>
        <a href="/link1">Link 1</a>
        <img src="/image1.jpg" alt="Image 1">
        </body></html>'''
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": ["https://crawler-test.com/link1"],
            "image_urls": ["https://crawler-test.com/image1.jpg"]
        }
        self.assertEqual(actual, expected)  
    # 
    def test_extract_page_data_missing_paragraphs(self):
        input_url = "https://crawler-test.com"
        input_body = '''<html><body>
        <h1>Test Title</h1>

        <a href="/link1">Link 1</a>
        <img src="/image1.jpg" alt="Image 1">
        </body></html>'''
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "Test Title",
            "first_paragraph": "",
            "outgoing_links": ["https://crawler-test.com/link1"],
            "image_urls": ["https://crawler-test.com/image1.jpg"]
        }
        self.assertEqual(actual, expected)
    #  
    def test_extract_page_data_missing_links(self):
        input_url = "https://crawler-test.com"
        input_body = '''<html><body>
        <h1>Test Title</h1>
        <p>This is the first paragraph.</p>

        <img src="/image1.jpg" alt="Image 1">
        </body></html>'''
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "Test Title",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": [],
            "image_urls": ["https://crawler-test.com/image1.jpg"]
        }
        self.assertEqual(actual, expected)
    #  
    def test_extract_page_data_missing_images(self):
        input_url = "https://crawler-test.com"
        input_body = '''<html><body>
        <h1>Test Title</h1>
        <p>This is the first paragraph.</p>
        <a href="/link1">Link 1</a>

        </body></html>'''
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "Test Title",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": ["https://crawler-test.com/link1"],
            "image_urls": []
        }
        self.assertEqual(actual, expected)
    # 

# 
if __name__ == "__main__":
    unittest.main()
