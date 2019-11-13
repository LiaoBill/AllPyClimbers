import requests
from bs4 import BeautifulSoup

# for time calculation
from time import time
from datetime import datetime

import re

import os

import json


def init_config_property():
    conff = open(
        "./config.json",
        "rt"
    )
    jsonstr = conff.read(-1)
    conf_context = json.loads(jsonstr)
    # print(conf_context['lg_position'])
    return conf_context


def log_out(str, conf_context):
    f = open(
        conf_context['lg_position'],
        "at",
        encoding="utf-8"
    )
    ct = datetime.now()
    pts = "[ LOG--" + ct.strftime('%Y-%m-%d-%H-%M-%S') + "] : " + str
    print(pts)
    f.write(pts + "\n")
    f.close()


def error_out(str, conf_context):
    f = open(
        conf_context['lg_position'],
        "at",
        encoding="utf-8"
    )
    ct = datetime.now()
    pts = "[ ERROR--" + ct.strftime('%Y-%m-%d-%H-%M-%S') + "] : " + str
    print(pts)
    f.write(pts + "\n")
    f.close()


def prepare_parameter(conf_context):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"
    headers = {
        'user-agent': user_agent
    }
    proxies = None
    if conf_context['is_proxies'] == "True":
        proxies = {
            'http': "192.168.1.104:10810",
            'https': "192.168.1.104:10810"
        }
    parameter = {
        'headers': headers,
        'proxies': proxies
    }
    return parameter

# funcs
# --------------------------------


def get_paper_name(cpaper_li):
    res_paper_name = ""
    article_sec = cpaper_li.find("article")
    if article_sec == None:
        return None
    title_span = article_sec.find("span", {
        "class": "title"
    })
    if title_span == None:
        return None
    res_paper_name = title_span.text
    if res_paper_name == "":
        return None
    return res_paper_name


def get_authors(cpaper_li):
    res_authors = []
    article_sec = cpaper_li.find("article")
    if article_sec == None:
        return None
    all_auth_spans = article_sec.find_all("span", {
        "itemprop": "author"
    })
    if len(all_auth_spans) == 0:
        return None
    for cauth in all_auth_spans:
        if cauth.text == "":
            continue
        res_authors.append(cauth.text)
    return res_authors


def get_doi_link(cpaper_li):
    navsec = cpaper_li.find("nav", {
        "class": "publ"
    })
    if navsec == None:
        return None
    doisec = navsec.find("li", {
        "class": "drop-down"
    })
    if doisec == None:
        return None
    doi_link = doisec.find("a", href=True)
    if doi_link == None:
        return None
    l = doi_link['href']
    if l == "":
        return None
    return l


def process_single_url(url, parameter, folder, conf_context):
    log_out("* STP URL == " + url, conf_context)

    # network process
    log_out("  * NetPccsing>>>>>>", conf_context)
    nst = time()
    try:
        response = requests.get(url, headers=parameter.get(
            'headers'), proxies=parameter.get('proxies'))
    except:
        return False
    ned = time()
    log_out(
        "  * NetPccsing Complete!___T-cst:{" + str((nst - ned)) + "}", conf_context)

    # prepare data process
    log_out("  * Pdpccsing>>>>>>", conf_context)
    pdpst = time()
    try:
        html = response.text
        soup = BeautifulSoup(html, features="html5lib")
    except:
        error_out("  * CREATE BEAUTIFUL SOUP ERROR!", conf_context)
        return False
    pdped = time()
    log_out(
        "  * Pdpccsing Complete!___T-cst:{" + str((pdped - pdpst)) + "}", conf_context)

    # data process
    log_out("  * PppsGetting>>>>>>", conf_context)
    ppsgst = time()
    all_paper_lis = soup.find_all("li", {
        "class": re.compile('entry (inproceedings|article)')
    })
    if len(all_paper_lis) == 0:
        error_out("  * SOUP FIND ALL \"LI\" RETURN EMPTY!", conf_context)
        return False
    required_s = []
    for cpaper_li in all_paper_lis:
        paper_name = None
        authors = []
        doi_link = None
        # get papername
        paper_name = get_paper_name(cpaper_li)
        if paper_name == None:
            error_out("    * !! papername can't fetch!", conf_context)
            paper_name = "[PAPER-NAME FETCH ERROR]"
        # get authors
        authors = get_authors(cpaper_li)
        if authors == None:
            error_out("    * paper [" + paper_name +
                      "] : authors can't fetch!", conf_context)
            authors = ["[CAN'T FETCH AUTHOR]"]
        # get doi link
        doi_link = get_doi_link(cpaper_li)
        if doi_link == None:
            error_out("    * paper [" + paper_name +
                      "] : doi-link can't fetch!", conf_context)
            doi_link = "[DOILINK : NOT-GET]"
        crs = {
            "paper_name": paper_name,
            "authors": authors,
            "doi_link": doi_link
        }
        required_s.append(crs)
    ppsged = time()
    log_out(
        "  * PppsGetting Complete!___T-cst:{" + str((ppsged - ppsgst)) + "}", conf_context)

    # get file title
    log_out("  * FTTLGetting>>>>>>", conf_context)
    fttlst = time()
    only_h1 = soup.find("h1")
    cconf_ppname = None
    if only_h1 == None:
        error_out("    * TTL NOT FETCHED, RANDOWM KEY INVOLVED !", conf_context)
        unique_id = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        cconf_ppname = "[TITLE-NOT-FETCHED]_" + unique_id
    else:
        cconf_ppname = only_h1.text

        def file_name_filter(cconf_ppname):
            v_res = ""
            for i in range(len(cconf_ppname)):
                if ord(cconf_ppname[i]) == 58:
                    break
                if 65 <= ord(cconf_ppname[i]) <= 90 or 97 <= ord(cconf_ppname[i]) <= 122 or 48 <= ord(cconf_ppname[i]) <= 57 or ord(cconf_ppname[i]) == 95 or ord(cconf_ppname[i]) == 45:
                    v_res += cconf_ppname[i]
            return v_res
        cconf_ppname = file_name_filter(cconf_ppname)
        unique_id = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        cconf_ppname += "[" + unique_id + "]"
    fttled = time()
    log_out(
        "  * FTTLGetting Complete!___T-cst:{" + str((fttled - fttlst)) + "}", conf_context)

    # write to file
    log_out("  * WTFProcessing>>>>>>", conf_context)
    wtfst = time()
    of = open(
        conf_context['paper_target_position'] +
        folder + "/" + cconf_ppname + ".md",
        "wt",
        encoding="utf-8"
    )
    of.write("# PC: " + str(len(required_s)) + "\n")
    for crs in required_s:
        paper_name = crs.get("paper_name")
        authors = crs.get("authors")
        doi_link = crs.get("doi_link")

        def get_paper_name_string(paper_name):
            return "[" + paper_name + "]"

        def get_auth_string(authors):
            s = "Authors: "
            for auth in authors:
                s += auth + ", "
            s = s[:-(len(", "))]
            return s

        def get_doi_link_string(doi_link):
            return "Doi: " + doi_link
        of.write(get_paper_name_string(paper_name) + "\n")
        of.write(get_auth_string(authors) + "\n")
        of.write(get_doi_link_string(doi_link) + "\n")
        of.write("----------------------------------------" + "\n")
    of.close()
    wtfed = time()
    log_out(
        "  * WTFProcessing Complete!___T-cst:{" + str((wtfed - wtfst)) + "}", conf_context)

    log_out("* FIN URL == " + url, conf_context)
    log_out("---------------------------------", conf_context)


def main_func():
    # read config
    conf_context = init_config_property()

    def clear_log(conf_context):
        f = open(
            conf_context['lg_position'],
            "wt",
            encoding="utf-8"
        )
        f.write("<LGSTART>" + "\n")
        f.close()
    clear_log(conf_context)
    proc_list = []

    fp = conf_context['url_data_position']
    all_fs = os.listdir(fp)

    def isolate_proc_urls(all_fs, conf_context):
        pclist = []
        pcclst = all_fs
        if conf_context['is_rlist'] == "True":
            pcclst = conf_context['rlst']
        # isolate urls
        for cf in pcclst:
            def isolate_url(cf, proc_list):
                try:
                    f = open(
                        conf_context['url_data_position'] + cf,
                        "rt"
                    )
                    cl = f.readlines()
                    f.close()
                    cl = [l.strip() for l in cl]
                    c_ulist = []
                    deep_level = int(conf_context['deep_level'])
                    if len(cl) < deep_level:
                        deep_level = len(cl)
                    for i in range(deep_level):
                        c_ulist.append(cl[i])
                    cproc = {
                        "url": c_ulist,
                        "folder": cf[:-(len(".md"))]
                    }
                    pclist.append(cproc)
                except Exception as e:
                    print(e)
                    return False
                return True
            if isolate_url(cf, proc_list) == False:
                error_out("PrewK___ISOLATE URLS ERROR", conf_context)
                return None
        log_out("PrewK___ISOLATE URLS READY!", conf_context)
        return pclist
    proc_list = isolate_proc_urls(all_fs, conf_context)

    def pre_mkdirs(all_fs, conf_context):
        pcclst = all_fs
        if conf_context['is_rlist'] == "True":
            pcclst = conf_context['rlst']
        for cf in pcclst:
            cpath = conf_context['paper_target_position'] + cf[:-(len(".md"))]
            try:
                if os.path.exists(cpath) == False:
                    os.mkdir(cpath)
            except:
                error_out("PrewK___MKDIRS ERROR!", conf_context)
                return
        log_out("PrewK___MKDIRS READY!", conf_context)
    pre_mkdirs(all_fs, conf_context)

    parameter = prepare_parameter(conf_context)
    for cproc in proc_list:
        cproc_target_url = cproc.get("url")
        for url in cproc_target_url:
            process_single_url(
                url, parameter, cproc.get("folder"), conf_context)


if __name__ == '__main__':
    main_func()
