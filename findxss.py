from functions import *
from functions import search_and_extract , progress
from concurrent.futures import ThreadPoolExecutor, wait,as_completed
event1 = threading.Event()

def main():
    try:
        con=False # continue aw la
        line_number=1
        num_of_processed_urls=0
        
        with open("progress.txt",'r+') as prog:
            progr=prog.readline()
            if progr:
                
                urlfile= search_and_extract("urlfile:","last_run.txt")
                num_of_threads = int(search_and_extract("num_of_threads:","last_run.txt"))
                Email = search_and_extract("Email:","last_run.txt")
                num_of_processed_urls = int(progress('/',progr))
                tot=int(total('/',progr))
                
                c = input(f"you have {tot-num_of_processed_urls} unfinshed job in {urlfile} do you want to continue?(y/n): ")
                
                if c == 'y':
                    
                    line_number = num_of_processed_urls
                    con=True
                
                else:    
                    while c != 'n' or c != 'y':
                        if c == 'y':
                            line_number = num_of_processed_urls
                            con=True
                        elif c == 'n':
                            break
                        c = input("please confirm your choice with 'y' for yes or 'n' for no \"case sensitive\" : ")   
                        
                
        if not con :
            print("IMPORTANT : urls should be formatted as follow :\"https://example.com?q=ok\" use use the \"does\" tool to format your urls properly")
            urlfile = input("File path: ")
            num_of_threads = int(input("nb of urls at the same time : "))
            Email = input("Email : ")
            with open("last_run.txt",'w') as lr:
                details=(f"urlfile:{urlfile}\nnum_of_threads:{num_of_threads}\nEmail:{Email}")
                lr.write(details)
            with open("progress.txt",'w') as p:
                p.write("calculating...")
        futures = [] 
        payloads = ['<yaali>', 'ya"ali\'', 'ya/ali' , '{ya{}ali}'] # ntibih l payload lezm ma yin3amallo detect eza fe escape character
        
        elapsed_time_thread = threading.Thread(target=measure_elapsed_time) # el processing time
        elapsed_time_thread.daemon = True
        elapsed_time_thread.start()
        
        submit_thread = threading.Thread(target=check_if_list_is_empty, args=(futures, event1,num_of_threads))# krmel ma shi yktob ma3 she bnfs l w2t
        submit_thread.daemon = True
        submit_thread.start()
        
        with open(urlfile, "r", encoding='utf-8') as uf:
            for _ in range(line_number - 1):
                uf.readline()
            urls = uf.readlines()
            len_of_file=len(urls) + (line_number - 1)
            
        event1.set()
        with ThreadPoolExecutor(max_workers=num_of_threads*num_of_threads) as executor:
            for url in urls:
                event1.wait()
                num_of_processed_urls+=1
                
                stat=f"{num_of_processed_urls}/{len_of_file}"
                
                with open("progress.txt",'w') as prog:
                    prog.write(stat)
                    
                for payload in payloads:
                    future=executor.submit(check_response,url, payload,Email,stat)
                    futures.append(future)
                    
                event1.clear()
        print(stat)
        with open("progress.txt",'w') as p:
            p.write('')
                
    except Exception as e:
        print(f"An error occurred: {e}")
        send_email(
            to_address = search_and_extract("Email:","last_run.txt"),
            subject="Progress Update",
            body=f"Job has been terminated unexpectedly : {urlfile}\nError: {e}"
            )
        
    except KeyboardInterrupt:
        print(f"shutting down please wait utill the already in process urls is done")
        executor.shutdown(wait=True)
               
if __name__ == "__main__":
    main()
    urlfile= search_and_extract("urlfile:","last_run.txt")
    send_email(
        to_address = search_and_extract("Email:","last_run.txt"),
        subject="Progress Update",
        body=f"Job is over : {urlfile}"
    )
    print("\nAll DONE !")