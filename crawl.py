from urllib.parse import urlsplit

def normalize_url(input_url):
    url_object = urlsplit(input_url)
    # 
    scheme, netloc, path, query, fragment = url_object
    # 
    output = f"{netloc}{path}"
    if output[-1] == "/":
        output = output[0:-1]
    # 
    return output 


if __name__ == "__main__":
    normalize_url()