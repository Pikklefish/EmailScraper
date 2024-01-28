### <<<Import necessary libraries>>> ###
from bs4 import BeautifulSoup  ##Used for webscraping (divided objects into python object trees)
import requests
import requests.exceptions
import urllib.parse
from collections import deque
import re  #Allows you to look for patterns in string (used to detect "@" patterns in email)
import pandas as pd
import os
from dotenv import load_dotenv
from email.message import EmailMessage
import ssl
import smtplib

##Prompt user for information
user_email = str(input("Sender email: "))
user_url = str(input("[+] Enter Target URL To Scan: "))
urls = deque([user_url])

scraped_urls = set()
emails = set()


count = 0
try: 
    while len(urls):
        count +=1
        if count == 100:  #will scrap the first 100 URLS from main page
            break
        url = urls.popleft()
        scraped_urls.add(url)

        parts = urllib.parse.urlsplit(url)
        base_url = '{0.scheme}://{0.netloc}'.format(parts)

        path = url[:url.rfind('/')+1] if '/' in parts.path else url
        
        print('[%d] Processing %s' % (count, url))

        try:
            response = requests.get(url) #looks for emails in response

        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
            continue #even after error: continue

        new_emails =set(re.findall(r'[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+', response.text, re.I)) ##Uses regex too look for email patterns
        emails.update(new_emails)

        soup = BeautifulSoup(response.text, features = "lxml")

        for anchor in soup.find_all("a"):
            link = anchor.attrs['href'] if 'href' in anchor.attrs else ''
            if link.startswith('/'):
                link = base_url + link
            elif not link.startswith('https'):
                link = path + link
            if not link in urls and not link in scraped_urls:
                urls.append(link)

except KeyboardInterrupt:
    print('[-] Closing!')


for mail in emails:
    print(mail)

emails_df = pd.DataFrame(sorted(emails), columns=["Emails"])  # Create a DataFrame from the sorted emails
emails_df.to_excel('emails.xlsx', index=False)  # Save the DataFrame to an Excel file



### <<< AUTOMATD EMAIL SENDING >>> ###
load_dotenv()
email_sender = user_email
email_password = os.getenv("GMAIL_KEY")
subject = ""
body = ""
in_body = False  # Flag to indicate if we're currently parsing the body section

with open('email_Template.txt', 'r') as file:
    for line in file:
        if line.startswith('SUBJECT:'):
            subject = line.strip().split('SUBJECT: ')[1]
        elif line.startswith('BODY:'):
            in_body = True  # Set the flag to True when BODY section starts
            body += line.strip().split('BODY: ')[1] + "\n"  # Start appending body text, if any, on the same line
        elif in_body:
            body += line  # Append subsequent lines to body, preserving formatting

# Now, `subject` and `body` contain the extracted information with preserved formatting for the body.

for email_receiver in emails:
    email_receiver = emails
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

context = ssl.create_default_context()

with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
    smtp.login(email_sender, email_password)
    smtp.sendmail(email_sender, email_receiver, em.as_string())
    print(f"Email sent to {email_receiver}")