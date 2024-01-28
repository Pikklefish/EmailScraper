# EmailScraper-Sender

## Main functionality
The program will accept a user inputed link and output an excel sheet of emails scraped from the link.


## How to get started
1. Clone/Fork or download the program file and open in IDE.

2. Download these libraries in your terminal <br>
    `pip3 install requests`<br>
    `pip3 install bs4`<br>
    `pip3 install BeautifulSoup`<br>
    `pip3 install lxml`<br>
    `pip install pandas openpyxl`

3. Follow propmts in the terminal.
4. Turn on 2 Step Verification for your Gmail account in setting
5. Go to `https://myaccount.google.com/apppasswords` and generate an app password names `python`.  16 character key will appear that python will use to access your gmail.
6. Rename the `.env_example` file to `.env` and fill in the `GMAIL_KEY`


A sample excel sheet consisting of emails from the `https://umich.edu/` is included.

**Do not use this project to conduct email attacks on any specific company or organization.**
This project is in refernece to "Building an Email Scraper Using Python 3 For Penetration Testing" by Aleksa Tamburkovski on Youtube.