import sys
# 
def main():
    sysArgs = sys.argv
    # 
    if len(sysArgs) < 2:
        print("no website provided")
        sys.exit(1)
    # 
    if len(sysArgs) > 2:
        print("too many arguments provided")
        sys.exit(1)
    # 
    BASE_URL = sysArgs[1]
    print(f"starting crawl of: {BASE_URL}")
    sys.exit(0)


if __name__ == "__main__":
    main()
