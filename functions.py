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

    print(f"Email sent successfully to {to_address}")

def check_response(url,payload,Email):# l ossa killa 
    newURL= appendPara(url,payload)
    response=requests.get(newURL)
    if payload in response.text:
        with output_lock:
            print(f"\rFound '{payload}' in the webpage {newURL}")
            with open("foundxss.txt",'a',encoding='utf-8') as xss:
                xss.write(newURL+'\n')
        send_email(Email,"XSS Finder Tool",f"Found possible XSS in this URL : {newURL}")
        
def measure_elapsed_time():# la ni3rif addeh akal w2t l program
    start_time = time.time()
    while True:
        elapsed_time = time.time() - start_time
        with output_lock:
            with open("progress.txt",'r') as pr:
                stat=pr.readline()
            print(f"\rElapsed time: {elapsed_time:.2f} seconds, under process urls: {stat}", end='', flush=True)
            time.sleep(0.1)
    
def check_if_list_is_empty(futures,event,num_of_threads):# krmel ma nfout b race condition
    while True:
        with lock:
            if len(futures)<=num_of_threads*num_of_threads:
                event.set()
            else:
                futures = [f for f in futures if not f.done()]# krmel nim7i mn l list le 5olso
