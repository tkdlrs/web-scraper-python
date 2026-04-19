import unittest
from crawl import normalize_url 

class Case:
    def __init__(self, i, e):
        self.i = i
        self.e = e


class TestCrawl(unittest.TestCase):
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
# 
if __name__ == "__main__":
    unittest.main()

