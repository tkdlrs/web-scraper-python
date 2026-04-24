import sys
from crawl import get_html
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
    request = get_html(base_url)
    print(request)
    print(f"crawl ended")
    # 
    sys.exit(0)


if __name__ == "__main__":
    main()
