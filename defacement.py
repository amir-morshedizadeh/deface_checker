# bc7db4fd365!/usr/bin/python3
# Author: Amir Morshedizadeh & Ali Ghayoumi
# Copywriter: Application Security Team @ SADAD Informatics Corporation 2022
from asyncio import events
import diff_match_patch as dmp_module
import re
import time
import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import logging
from os.path import exists
import os
from urllib.parse import urlparse
import urllib3
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import threading
import html
from urllib3.connectionpool import xrange
import uuid
import glob

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
telegram_auth_token = "632450292:APZLrOJJptfjQfgjOrTDfL9OnPl5rGGt16zZr1bW"
telegram_group_id_defacement = "7784145"
telegram_group_id_unavailable = "1477573755"
telegram_api_url = f"https://tapi.bale.ai/bot{telegram_auth_token}/sendMessage"
headers = {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'}
base_dir = "E:\\root\\"
user_agent = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'}
websites = []

def main():
    setup()
    while True:
        for website in websites:
            time.sleep(2.3)
            #threads = []
            #with ThreadPoolExecutor(max_workers=1) as executor:
            #    threads.append(executor.submit(send_req, website))
            send_req(website)


def requests_retry_session(retries=2, backoff_factor=5, session=None):
    session = session or requests.Session()
    retry = Retry(total=retries, read=retries, connect=retries, backoff_factor=backoff_factor)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


def setup():
    try:
        session = requests_retry_session(retries=2)
        with open(base_dir + "urls.txt", "r", encoding="utf-8", newline='') as file_urls:
            temp = file_urls.read().splitlines()
            for url in temp:
                url_domain = urlparse(url).netloc
                url_dir = base_dir + url_domain + urlparse(url).path.replace("/", "_")
                websites.append([url_dir, url])
                if not exists(url_dir):
                    os.makedirs(url_dir, exist_ok=True)
                html_file = glob.glob(url_dir + '\\' + '*.html')
                for filepath in html_file:
                    try:
                        os.remove(filepath)
                    except:
                        print("no HTML file")
                if not exists(url_dir + '\\page_old.txt'):
                    try:
                        r = session.get(url, allow_redirects=True, timeout=8, verify=False, headers=user_agent)
                    except BaseException as err1:
                        print("setup: "+str(err1))
                    if r.status_code == 200:
                        with open(url_dir + '\\page_old.txt', 'w+', encoding='utf-8', newline='') as file_page:
                            file_page.write(r.text)
                    else:
                        print("The response code is: " + str(r.status_code) + " for " + url)
                        msg = url + "\n\n" + "The response code is: " + str(r.status_code)
                        send_message_for_services(msg)
    except BaseException as err:
        print("setup: "+str(err))


def send_message_for_defacement(msg):
    """
    + Sends "msg" via a Telegram Bot to a Telegram Group for any defacement alarm
    """
    session = requests_retry_session(retries=5)
    try:
        content = {'chat_id': telegram_group_id_defacement, 'text': msg}
        session.post(telegram_api_url, json=content, headers=headers, timeout=15, allow_redirects=True)
    except BaseException as err:
        print("send_message_for_defacement():  " + str(err))


def send_message_for_services(msg):
    """
    + Sends "msg" via a Telegram Bot to a Telegram Group for monitoring service availability
    """
    session = requests_retry_session(retries=5)
    try:
        content = {'chat_id': telegram_group_id_unavailable, 'text': msg}
        session.post(telegram_api_url, json=content, headers=headers, timeout=15, allow_redirects=True)
    except BaseException as err:
        print("send_message_for_services:  " + str(err))


def filtering(text, url_dir):
    soup__tmp = BeautifulSoup(text, 'html.parser', multi_valued_attributes=None)
    if exists(url_dir + "\\whitelist_" + ".txt"):
        with open(url_dir + "\\whitelist_" + ".txt", "r", encoding="utf-8", newline='') as file_whitelist:
            exceptions = file_whitelist.read().splitlines()
        if len(exceptions) == 0:
            return
        for line in exceptions:
            try:
                if len(line) > 0:
                    x = line.split(",")
                    y = x[1].split(":")
                    if len(x) == 2:
                        t = soup__tmp.find(x[0], {y[0]: y[1]})
                        if t:
                            t.decompose()
                    elif len(x) == 3 and x[2] == "regex":
                        t = soup__tmp.find(x[0], {y[0]: re.compile(y[1])})
                        if t:
                            t.decompose()
                    elif len(x) == 3 and x[2] == "regexstring":
                        t = soup__tmp.find(x[0], string=re.compile(y[1]))
                        if t:
                            t.string = re.sub(y[1], '', t.text)
                    elif len(x) == 4 and x[3] == "replaceattr":
                        t = soup__tmp.find(x[0], {y[0]: re.compile(y[1])})
                        z = x[2].split(":")
                        if t:
                            t.attrs[z[0]] = z[1]
            except BaseException as err:
                print(err)
    text = str(soup__tmp.prettify())
    return text


def send_req(website):
    """
    + Sends the request to the site and saves the response(status code 200) into the "text2" variable.
    + If the response is other than 200, it sends received code via "send_message_for_services()" to the Telegram bot.
    + Reads "page.txt" and saves the content to "text1" variable.
    + Compares "new.txt" known as "text1" WITH the latest response of the site known as "text2".
    + If they are not same, it sends both "text1" and "text2" to "compare()" to find all changes of the site.
    """
    url_dir = website[0]
    url = website[1]
    session = requests_retry_session(retries=5)
    try:
        with open(url_dir + '\\page_old.txt', 'r', encoding='utf-8', newline='') as old_page:
            text1 = old_page.read()
        r = session.get(url, allow_redirects=True, timeout=15, verify=False, headers=user_agent)
        if r.status_code == 200:
            text2 = r.text
            with open(url_dir + '\\page.txt', 'w+', encoding='utf-8', newline='') as file_page:
                file_page.write(text2)
            if text1 != text2:
                with open(url_dir + '\\page_old.txt', 'w+', encoding='utf-8', newline='') as old1_page:
                    old1_page.write(text2)
                compare(text1, text2, url_dir, url)
        else:
            print("The response code is: " + str(r.status_code) + " for " + url)
            msg = url + "\n\n" + "The response code is: " + str(r.status_code)
            send_message_for_services(msg)
    except BaseException as err:
        print("send_req():"+str(err) + " URL=" + url)


def compare(text1, text2, url_dir, url):
    """
    + At first it sends "text1" and "text2" to filtering() for applying exceptions(False Positive) for each site.
    + Then it compares "text11" and "text22" for the equality
    + If not same, it means there are some changes.
    + "diff_match_patch" python library is used for finding ADDED and REMOVED parts of changes with the highlighted color.
    + Red highlight is used for showing REMOVED parts and Green highlight is used for ADDED parts.
    + The result of the compare is saved to a random HTML file for sending to the Telegram group via the Telegram Bot.
    """
    text11 = filtering(text1, url_dir)
    text22 = filtering(text2, url_dir)
    if text11 == text22:
        return
    dif = dmp_module.diff_match_patch()
    dif_result = dif.diff_main(text11, text22, False, 10)
    dif.diff_cleanupSemantic(dif_result)
    html_result = dif.diff_prettyHtml(dif_result)
    soup = BeautifulSoup(html_result, 'html.parser')
    added = [a.get_text() for a in soup.find_all('ins')]
    removed = [a.get_text() for a in soup.find_all('del')]
    unique_file_name = str(uuid.uuid4())
    if added or removed:
        html_file = glob.glob(url_dir + "\\" + "*.html")
        for filepath in html_file:
            try:
                os.remove(filepath)
            except:
                print("no HTML file")
        with open(url_dir + "\\" + unique_file_name + ".html", 'w+', encoding='utf-8', newline='') as file_alert:
            for i in xrange(len(added)):
                file_alert.write("<ins style=\"background:#e6ffe6;\">" + html.escape(added[i]) + "<br>" + "</ins>")
            for i in xrange(len(removed)):
                file_alert.write("<del style=\"background:#ffe6e6;\">" + html.escape(removed[i]) + "<br>" + "</del>")
            file_alert.write("<br></br>\n")
            file_alert.write(html_result)
    url_domain = urlparse(url).netloc
    changes_file = "https://defacement.sadad.co.ir/" + url_domain + urlparse(url).path.replace("/", "_") + "/" + unique_file_name + ".html"
    msg = url + "\n\n" + changes_file
    send_message_for_defacement(msg)
    return

if __name__ == "__main__":
    main()
