import sys
from crawl import crawl_page
# 
def main():
    args = sys.argv
    # 
    if len(args) < 2:
        print("no website provided")
        sys.exit(1)
    # 
    if len(args) > 2:
        print("too many arguments provided")
        sys.exit(1)
    # 
    base_url = args[1]
    # 
    print(f"starting crawl of: {base_url}")
    # 
    rich_data = {}
    try:
        crawl_page(base_url, base_url, rich_data)
    except Exception as e:
        print(f"Error fetching HTML from {base_url}: {str(e)}")
        sys.exit(1)
    # 
    print(f"You have crawled {len(rich_data)} pages")
    # 
    print(f"crawl ended")
    # 
    sys.exit(0)


if __name__ == "__main__":
    main()
