from functions import *
from functions import search_and_extract , progress
from concurrent.futures import ThreadPoolExecutor, wait,as_completed
from termcolor import colored

event1 = threading.Event()
flag = threading.Event()


def main():
    try:
        logo()
        con=False # continue aw la
        line_number=1
        num_of_processed_urls=0
        
        with open("progress.txt",'r+') as prog:
            progr=prog.readline().strip()
            if progr:
                 
                urlfile= search_and_extract("urlfile:","last_run.txt")
                num_of_threads = int(search_and_extract("num_of_threads:","last_run.txt"))
                Email = search_and_extract("Email:","last_run.txt")
                num_of_processed_urls = int(progress('/',progr))
                tot=int(total('/',progr))
                
                c = input(
                            colored(f"you have ",'blue')+
                            colored(f"({tot-num_of_processed_urls})",'red')+
                            colored(f" unfinshed job in {urlfile} do you want to continue?(y/n): ","blue")
                        )
                
                if c == 'y':
                    
                    line_number = num_of_processed_urls
                    con=True
                
                else:    
                    while c != 'n' or c != 'y':
                        if c == 'y':
                            line_number = num_of_processed_urls
                            con=True
                        elif c == 'n':
                            a = input(colored("please confirm your choice with 'y' for yes or 'n' for no : ",'light_red'))   
                            if a == "n":
                                break
                        c = input(colored("please confirm your choice with 'y' for yes or 'n' for no \"case sensitive\" : ",'light_red'))   
                        
                
        if not con :
            print(
                  colored("IMPORTANT :",'light_red') + 
                  colored(" urls should be formatted as follow :",'white')+ 
                  colored(" \"https://example.com?q=ok\" ",'dark_grey') +
                  colored("you can use the \"does\" tool to format your urls properly\n",'white')
                  )
            with open('foundxss.txt','r') as fr:
                found=None
                found=fr.readline()
                if found :
                    erase=input(colored("There are previous findings in the 'foundxss.txt' file. Do you want to overwrite them? Choosing 'n' will append the new findings to the previous ones (y/n): ",'dark_grey'))
                    if erase == 'y':
                        erase2=input(colored("Are you sure you want to delete the content of 'foundxss.txt': ",'red'))
                        if erase2=='y':
                            with open('foundxss.txt','w') as fw:
                                fw.write('')
                    
            urlfile = input(colored("\nFile path: ",'cyan'))
            num_of_threads = int(input(colored("nb of urls at the same time : ",'cyan')))
            Email = input(colored("Email : ",'cyan'))
            num_of_processed_urls= 0
            with open("last_run.txt",'w') as lr:
                details=(f"urlfile:{urlfile}\nnum_of_threads:{num_of_threads}\nEmail:{Email}")
                lr.write(details)
            ini_stat=f"\ncalculating please wait ...\n"
            print("\r"+colored(ini_stat,'light_yellow'))
        futures = []
        payloads = ['<yaali>','<a>yaali', 'ya"ali\'', 'ya/ali' , 'ya{}ali'] # ntibih l payload lezm ma yin3amallo detect eza fe escape character
        
        elapsed_time_thread = threading.Thread(target=measure_elapsed_time, args=(flag,) ) # el processing time
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
                
                colored_stat=colored(f"( {num_of_processed_urls}",'cyan')+" / "+colored(f"{len_of_file} )",'cyan')
                stat=f"{num_of_processed_urls}/{len_of_file}"
                
                with progress_lock:
                    with open("progress.txt",'w') as prog:
                       prog.write(stat)
                    
                for payload in payloads:
                    future=executor.submit(check_response,url, payload,Email,colored_stat)
                    futures.append(future)
                    
                event1.clear()
        with progress_lock:
            with open("progress.txt",'w') as p:
                p.write('')
                
    except Exception as e:
        with output_lock:
            print(f"An error occurred: {e}")
        with lock:
            send_email(
                to_address = search_and_extract("Email:","last_run.txt"),
                subject="Progress Update",
                body=f"Job has been terminated unexpectedly : {urlfile}\nError: {e}"
                )
        
    except KeyboardInterrupt:
        with output_lock:
            print(colored("\rshutting down please wait utill the already in process urls is done",'light_red'))
        executor.shutdown(wait=True)
        
    flag.set()
    elapsed_time_thread.join()
    print(colored_stat,flush=True)
    urlfile= search_and_extract("urlfile:","last_run.txt")
    send_email(
        to_address = search_and_extract("Email:","last_run.txt"),
        subject="Progress Update",
        body=f"Job is over : {urlfile}"
    )
    
if __name__ == "__main__":
    main()
    print(colored("\nAll DONE !\n",'light_green'))
