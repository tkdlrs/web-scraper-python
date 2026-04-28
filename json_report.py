import json 

# 
def write_json_report(page_data, filename="report.json"):
    # 
    pages = sorted(page_data.values(), key=lambda p: p["url"])
    try: 
        with open(filename, 'w', encoding="utf-8") as file:
            json_content = json.dump(pages, file, indent=2)
            file.write(str(json_content))
    except Exception as e:
        print(f"Error:  {e}")
    # 
    return
