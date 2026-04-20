import unittest 
from extract import get_heading_from_html, get_first_paragraph_from_html

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
    # 
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
    # 