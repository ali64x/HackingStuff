from functions import *

def main():
    try:
        urlfile = input("Enter the urls file path: ")
        
        elapsed_time_thread = threading.Thread(target=measure_elapsed_time)
        elapsed_time_thread.daemon = True
        elapsed_time_thread.start()
        
        with open(urlfile, "r", encoding='utf-8') as uf:
            urls = uf.readlines()
            
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = []
            for url in urls:
                future = executor.submit(search_for_xss_and_report,url)
                futures.append(future)
            wait(futures)
            
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
    print("\nAll DONE !")