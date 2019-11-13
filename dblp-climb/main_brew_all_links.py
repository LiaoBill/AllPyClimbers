import requests
from bs4 import BeautifulSoup

# for time calculation
from time import time
from datetime import datetime


url_file_path = "./eccv_a.md"

url_list = []


def assign_url_list(list):
    global url_list
    url_list = list
    url_list = [url.strip() for url in url_list]


def get_url_list():
    global url_list
    return url_list


def log_out(str):
    ct = datetime.now()
    print("[ LOG--" + ct.strftime('%Y-%m-%d-%H-%M-%S') + "] : " + str)


def error_out(str):
    ct = datetime.now()
    print("[ ERROR--" + ct.strftime('%Y-%m-%d-%H-%M-%S') + "] : " + str)


def read_url_list(url_file_path):
    try:
        f = open(
            url_file_path,
            "rt"
        )
        assign_url_list(f.readlines())
        f.close()
        return True
    except:
        return False


def prepare_parameter():
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"
    headers = {
        'user-agent': user_agent
    }
    parameter = {
        'headers': headers,
    }
    return parameter


def fetch_url_conf_list(url, parameter):
    # all time
    all_start = time()

    log_out("* START PROCESS url == " + url)

    # network part
    log_out("  * network processing ... ")
    nts = time()
    try:
        response = requests.get(url, headers=parameter.get('headers'))
    except:
        return False
    nte = time()
    log_out("  * network complete! " + "[time cost : " + str(nte-nts) + "]")

    # data processing
    log_out("  * processing ... ")
    pts = time()
    # get a href list
    try:
        html = response.text
        soup = BeautifulSoup(html, features="html5lib")
    except:
        error_out("  * CREATE BEAUTIFUL SOUP ERROR!")
        return False
    all_a = soup.find_all("a", href=True)
    if len(all_a) == 0:
        error_out("  * SOUP FIND ALL \"A\" RETURN EMPTY!")
        return False
    required_a = []
    filter_url = url
    if filter_url.endswith("index.html") == True:
        filter_url = filter_url[:-(len("index.html"))]
    for a in all_a:
        ch = a['href']
        if ch.startswith(filter_url) == True:
            required_a.append(a)
    res = []
    for a in required_a:
        ch = a['href']
        res.append(ch)
    # get current conf name
    only_h1 = soup.find("h1")
    if only_h1 == None or only_h1 == "":
        error_out("  * FIND H1 TITLE EMPTY!")
        return False
    title_string = only_h1.text.replace("\n", " ").replace("/", "-")
    pte = time()
    log_out("  * process complete! " + "[time cost : " + str(pte-pts) + "]")

    # output to file
    log_out("  * write to file processing ... ")
    try:
        tf = open(
            "./" + title_string + ".md",
            "wt"
        )
        for ra in res:
            tf.write(ra + "\n")
        tf.close()
    except:
        error_out("  * WRITE FILE ERROR!")
        return False
    log_out("  * write to file completed!")

    all_end = time()
    log_out("* START PROCESS url == " + url + " COMPLETED! " +
            "[time cost : " + str(all_end - all_start) + "]")
    return True


def main_func():
    if read_url_list(url_file_path) == False:
        print("READ FILE ERROR")
        return
    parameter = prepare_parameter()
    for url in get_url_list():
        cstatus = fetch_url_conf_list(url, parameter)
        if cstatus == False:
            break


if __name__ == '__main__':
    main_func()
