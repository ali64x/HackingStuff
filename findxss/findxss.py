from .functions import *
from .functions import search_and_extract , progress
from concurrent.futures import ThreadPoolExecutor, wait,as_completed
from termcolor import colored
import argparse
import re


event1 = threading.Event()
flag = threading.Event()


def main():
    try:
        logo()
        parser = argparse.ArgumentParser(description="Mining URLs from dark corners of Web Archives ")
        parser.add_argument("-e", "--email", help="email you want to send results and update to.",default=False)
        parser.add_argument("-l", "--list", help="File containing a list of urls.")
        parser.add_argument("-c", "--conPreRun", help="continue previouse work if exist takes (y/n) arguments only .",default=False)
        parser.add_argument("-o", "--output", help="output file path. Default is foundxss.txt file  in the same directory.", default='findxss/foundxss.txt')
        parser.add_argument("-n", "--NumberOfUrls", help="number of processed urls per at once 'threads= n*n'.",default=5)
        args = parser.parse_args()
        
        con=False # continue aw la
        line_number=1
        num_of_processed_urls=0
        with open("findxss/progress.txt",'r+') as prog:
            progr=prog.readline().strip()
            if progr:
                 
                urlfile= search_and_extract("urlfile:","findxss/last_run.txt")
                num_of_threads = int(search_and_extract("num_of_threads:","findxss/last_run.txt"))
                Email = search_and_extract("Email:","findxss/last_run.txt")
                num_of_processed_urls = int(progress('/',progr))
                if search_and_extract("outputfile:","findxss/last_run.txt"):
                    outputfile=search_and_extract("outputfile:","findxss/last_run.txt")
                tot=int(total('/',progr))
                if args.conPreRun :
                    c = args.conPreRun
                    print(
                        colored(f"you have ",'blue')+
                        colored(f"({tot-num_of_processed_urls})",'red')+
                        colored(f" unfinshed job in {urlfile} ","blue")
                        )
                else:
                    c = input(
                                colored(f"you have ",'blue')+
                                colored(f"({tot-num_of_processed_urls})",'red')+
                                colored(f" unfinshed job in {urlfile} do you want to continue?(y/n): ","blue")
                            )
                
                if c == 'y':
                    
                    line_number = num_of_processed_urls
                    con=True
                    
                elif c == 'n':
                    pass
                
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
                                    
            if  len(sys.argv) == 1 or "-h" in sys.argv[1:] : #if no argument is passed or -h is present, show this
                urlfile = input(colored("\nFile path: ",'cyan'))
                num_of_threads = input(colored("nb of urls at the same time (default is 5) : ",'cyan'))
                if not num_of_threads:
                    num_of_threads = 5
                else:
                    num_of_threads = int(num_of_threads)
                Email = input(colored("Email : ",'cyan'))
                outputfile = input(colored("Output File (default is foundxss.txt) : ", 'cyan'))
                if not outputfile :
                    outputfile="findxss/foundxss.txt"
                    print (colored ("[*] Output file set to "+outputfile, 'yellow'))
            else:
                urlfile=args.list
                num_of_threads=int(args.NumberOfUrls)
                Email = args.email
                outputfile = args.output
                        
            # check if user wants to delete the default output file or append to it 
            
            if outputfile == "findxss/foundxss.txt" :
                with open('findxss/foundxss.txt','r') as fr:
                    found=None
                    found=fr.readline()
                    if found :
                        erase=input(colored("There are previous findings in 'foundxss.txt' file. Do you want to overwrite them? Choosing 'n' will append the new findings to the previous ones (y/n): ",'dark_grey'))
                        if erase == 'y':
                            erase2=input(colored("Are you sure you want to delete the content of 'foundxss.txt': ",'red'))
                            if erase2=='y':
                                with open('findxss/foundxss.txt','w') as fw:
                                    fw.write('')
                                    
            num_of_processed_urls= 0
            with open("findxss/last_run.txt",'w') as lr:
                details=(f"urlfile:{urlfile}\nnum_of_threads:{num_of_threads}\nEmail:{Email}\noutputfile:{outputfile}")
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
                    with open("findxss/progress.txt",'w') as prog:
                       prog.write(stat)
                    
                for payload in payloads:
                    future=executor.submit(check_response,url, payload,colored_stat,outputfile,Email)
                    futures.append(future)
                    
                event1.clear()
        with progress_lock:
            with open("findxss/progress.txt",'w') as p:
                p.write('')
                
    except Exception as e:
        with output_lock:
            print(f"An error occurred: {e}")
        with lock:
            if Email:
                send_email(
                    to_address = search_and_extract("Email:","findxss/last_run.txt"),
                    subject="Progress Update",
                    body=f"Job has been terminated unexpectedly : {urlfile}\nError: {e}"
                    )
        
    except KeyboardInterrupt:
        with output_lock:
            print(colored("\rshutting down please wait utill the already in process urls is done",'light_red'))
        if executor:
            executor.shutdown(wait=True)
        
    flag.set()
    elapsed_time_thread.join()
    print(colored_stat,flush=True)
    urlfile= search_and_extract("urlfile:","findxss/last_run.txt")
    if Email:
        send_email(
            to_address = search_and_extract("Email:","findxss/last_run.txt"),
            subject="Progress Update",
            body=f"Job is over : {urlfile}"
        )
        
    print(colored("\nAll DONE !\n",'light_green'))

    
if __name__ == "__main__":
    main()
