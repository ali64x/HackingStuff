import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
from concurrent.futures import ThreadPoolExecutor, wait,as_completed
import time
import threading
output_lock = threading.Lock() # krmel l threads ma yiktbo ma3 ba3d w y5arrbo l dinya
lock=threading.Lock()

def appendPara(original_string, append_string): # la n3abbi l payload
    return original_string[:-1] + append_string

def send_email(to_address, subject, body):# wad7a la nib3at email
    
    sender_email = 'auto83851@gmail.com'
    sender_password = 'zmiu chxr kfiq sftr'
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587  # Use 465 for SSL

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_address
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_address, msg.as_string())

    print(f"\rEmail sent successfully to {to_address}")

def check_response(url,payload,Email,stat,tries=0,time=30):# l ossa killa 
    try:
        newURL= appendPara(url,payload)
        response=requests.get(newURL,timeout=time)
        html_content = response.text  # Use response.content for binary content
        with output_lock:
            print (stat.strip(),end='\r')
        if html_content:
            if payload in html_content:
                with output_lock:
                    print(f"\rFound '{payload}' in the webpage {newURL}")
                    with open("foundxss.txt",'a',encoding='utf-8') as xss:
                        xss.write(newURL+'\n')
                send_email(Email,"XSS Finder Tool",f"Found possible XSS in this URL : {newURL}")
        else:
            if tries < 15:
                check_response(url,payload,Email,stat,tries+1)
                time.sleep(0.5)
    except :
        with lock:
           with open("exceptions.txt",'r+') as e:
              filelines=e.readlines().strip()
              if url not in filelines: 
                  e.write(url)
            
def measure_elapsed_time():# la ni3rif addeh akal w2t l program
    start_time = time.time()
    while True:
        elapsed_time = time.time() - start_time
        with output_lock:
            print(f"\rElapsed time: {elapsed_time:.2f} seconds, under process url number: ", end='', flush=True)
            time.sleep(0.1)
    
def check_if_list_is_empty(futures,event,num_of_threads):# krmel ma nfout b race condition
    while True:
            if len(futures) <= num_of_threads*num_of_threads:
                event.set()
            else:
                event.clear()                   
                new_futures = []
                for f in futures:                        # krmel nim7i mn l list le 5olso
                    if not f.done():
                        new_futures.append(f)
                futures = new_futures
                
def search_and_extract(key, file_path):
    try:
        with open(file_path, 'r') as file:
            for line in file:
                index = line.find(key)
                if index != -1:
                    result=(line[index + len(key):].strip())
                    return result
    except FileNotFoundError:
        print(f"\rFile not found: {file_path}")
    
def progress (key, string):
    index = string.find(key)
    if index != -1:
        result=(string[:index].strip())
        return result
    
def total (key, string):
    index = string.find(key)
    if index != -1:
        result=(string[index+1:].strip())
        return result
    
    
