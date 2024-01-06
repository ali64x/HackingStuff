import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
from concurrent.futures import ThreadPoolExecutor, wait
import sys
import time
import threading    

def appendPara(original_string, append_string):
    return original_string[:-1] + append_string

def send_email(to_address, subject, body):
    # Email configuration (replace placeholders with your information)
    sender_email = 'auto83851@gmail.com'
    sender_password = 'zmiu chxr kfiq sftr'
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587  # Use 465 for SSL

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_address
    msg['Subject'] = subject

    # Attach the body of the email
    msg.attach(MIMEText(body, 'plain'))

    # Establish a connection to the SMTP server
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        # Start the TLS connection
        server.starttls()

        # Login to the email account
        server.login(sender_email, sender_password)

        # Send the email
        server.sendmail(sender_email, to_address, msg.as_string())

    print(f"Email sent successfully to {to_address}")

def search_for_xss_and_report(url):
    payloads = ['<yaali>', '"yaali\'', '/yaali', 'yaali;', '{yaali}']
    futures=[]
    with ThreadPoolExecutor(max_workers=len(payloads)) as executor:
        for payload in payloads:
           future = executor.submit(check_response, url, payload)
           futures.append(future)
        wait(futures)

def check_response(url,payload):
    newURL= appendPara(url,payload)
    response=requests.get(newURL)
    if payload in response.text:
        with open("foundxss.txt",'a',encoding='utf-8') as xss:
            xss.write(newURL+'\n')
        print(f"\rFound '{payload}' in the webpage {newURL}")
        # send_email("htlr780@gmail.com","XSS Finder Tool",f"Found XSS in this URL : {newURL}") # substitute the email adress with your own gmail
        
def measure_elapsed_time():
    start_time = time.time()
    while True:
        elapsed_time = time.time() - start_time
        print(f"\rElapsed time: {elapsed_time:.2f} seconds", end='', flush=True)
        time.sleep(0.1)