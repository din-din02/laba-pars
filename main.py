import time
from class_parsing import Parser

def main():
    open("py_log.txt", "w", encoding="utf-8").close()
    
    a = Parser()

    a.proxy()

    a.processing()
    time.sleep(1)

    a.watch_parametrs()
    time.sleep(1)

    a.get_links_on_page()
    time.sleep(1)

    a.go_to_the_next_page()
    time.sleep(1)
    
    a.get_links_on_page()
    time.sleep(1)
    
    a.get_info()
    
    a.save_with_pandas()
    

if __name__ == "__main__":
    main()
