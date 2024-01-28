### <<<Import necessary libraries>>> ###
from bs4 import BeautifulSoup  ##Used for webscraping (divided objects into python object trees)
import requests
import requests.exceptions
import urllib.parse
from collections import deque
import re  #Allows you to look for patterns in string (used to detect "@" patterns in email)
import pandas as pd

#Prompt user for information
user_url = str(input("[+] Enter Target URL To Scan: "))
urls = deque([user_url])

scraped_urls = set()
emails = set()


count = 0
try: 
    while len(urls):
        count +=1
        if count == 100:
            break
        url = urls.popleft()
        scraped_urls.add(url)

        parts = urllib.parse.urlsplit(url)
        base_url = '{0.scheme}://{0.netloc}'.format(parts)

        path = url[:url.rfind('/')+1] if '/' in parts.path else url
        
        print('[%d] Processing %s' % (count, url))

        try:
            response = requests.get(url)

        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
            continue

        new_emails =set(re.findall(r'[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+', response.text, re.I))
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

