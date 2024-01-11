from functions import *
from concurrent.futures import ThreadPoolExecutor, wait,as_completed
event1 = threading.Event()

def main():
    try:
        with open("progress.txt",'w') as prog:
                    prog.write("calculating...")
        num_of_processed_urls = 0
        print("IMPORTANT : urls should be formatted as follow :\"https://example.com?q=ok\" use use the \"does\" tool to format your urls properly")
        urlfile = input("File path: ")
        num_of_threads = int(input("nb of urls at the same time : "))
        Email = input("Email :")
        futures = []
        payloads = ['<yaali>', 'ya"ali\'', 'ya/ali' , '{ya{}ali}']
        
        elapsed_time_thread = threading.Thread(target=measure_elapsed_time)
        elapsed_time_thread.daemon = True
        elapsed_time_thread.start()
        
        submit_thread = threading.Thread(target=check_if_list_is_empty, args=(futures, event1,num_of_threads))
        submit_thread.daemon = True
        submit_thread.start()
        
        with open(urlfile, "r", encoding='utf-8') as uf:
            urls = uf.readlines()
            len_of_file=len(urls)
            
        event1.set()
        with ThreadPoolExecutor(max_workers=num_of_threads*num_of_threads) as executor:
            for url in urls:
                event1.wait()
                for payload in payloads:
                    future=executor.submit(check_response,url, payload,Email)
                    futures.append(future)
                event1.clear()
                num_of_processed_urls+=1
                stat=f"{num_of_processed_urls}/{len_of_file}"
                with open("progress.txt",'w') as prog:
                    prog.write(stat)
                
    except Exception as e:
        print(f"An error occurred: {e}")
            
if __name__ == "__main__":
    main()
    print("\nAll DONE !")