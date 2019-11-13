import requests
from bs4 import BeautifulSoup

# for time calculation
from time import time
from datetime import datetime

url_list = []


def assign_url_list(list):
    global url_list
    url_list = list
    url_list = [url.strip() for url in url_list]


def get_url_list():
    global url_list
    return url_list


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
    try:
        response = requests.get(url, headers=parameter.get('headers'))
    except:
        return False

    # data processing
    # get a href list
    try:
        html = response.text
        soup = BeautifulSoup(html, features="html5lib")
    except:
        return False
    # get current conf name
    only_h1 = soup.find("h1")
    if only_h1 == None or only_h1 == "":
        return False
    title_string = only_h1.text.replace("\n", " ").replace("/", "-")

    # output to file
    try:
        tf = open(
            "./all_p.md",
            "at"
        )
        tf.write(title_string + "\n")
        tf.close()
    except:
        return False
    return True


def main_func():
    url_file_path = "./all_a.md"
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
