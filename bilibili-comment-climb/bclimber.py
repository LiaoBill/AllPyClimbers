import json
import math
import os
import re
from datetime import datetime
from time import time

import requests
from bs4 import BeautifulSoup

from utils import error_out, log_out, outptjson, readjson, set_lg_file


def prepare_parameter():
  user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"
  headers = {
    'user-agent': user_agent
  }
  parameter = {
    'headers': headers
  }
  return parameter

def set_url():
  url_base = "https://api.bilibili.com/x/v2/reply?"
  url_parameters = {
    'jsonp': 'jsonp',
    'type': '1',
    'sort': '2',
    'oid': '72003009',
    'pn': ''
  }
  url = url_base
  for key in url_parameters:
    url += (key + "=" + url_parameters[key] + "&")
  url = url[:-1]
  print(url)
  return url

def main_func():
  def check_success(level, target_dt, str):
    if target_dt == None:
      str = str.ljust(50-level*2, "-")
      error_out(level, str + "[__ F A I L E D __]")
      return False
    else:
      str = str.ljust(50-level*2, "-")
      log_out(level, str + "[_ S U C C E S S _]")
      return True
  def request_json(url):
    parameter = prepare_parameter()
    try:
      response = requests.get(url, headers=parameter.get('headers'))
    except:
      error_out(0, "NETWORK REQUEST")
      return None
    dt = None
    try:
      jsonstr = response.text
      dt = json.loads(jsonstr)
      return dt
    except:
      error_out(0, "PARSING JSON OBJECT")
      return None
  def get_whole_page_count(meta_pg):
    try:
      page_info = meta_pg['data']['page']
      all_comment_count = int(page_info['count'])
      each_page_size = 20
      whole_page_count = math.ceil(all_comment_count/each_page_size)
      return whole_page_count
    except:
      error_out(1, "Requesting meta page.")
      return None
  def get_current_url(i):
    current_page_number = i + 1
    current_url = global_url + str(current_page_number)
    return current_url

  # set log file
  set_lg_file("./", "log.md")

  global_url = set_url()

  # network
  log_out(0, "Network processing>>>>>>>>")

  # meta page for page count
  log_out(1, "Requesting meta page.")
  meta_pg = None
  meta_pg = request_json(get_current_url(0))
  if check_success(2, meta_pg, "Requesting meta page") == False:
    return False
  log_out(1, "Calculating page count.")
  whole_page_count = get_whole_page_count(meta_pg)
  if check_success(2, whole_page_count, "Caculate page count") == False:
    return False
  log_out(2, "Page Count is: " + str(whole_page_count))


  if whole_page_count <= 0:
    error_out(1, "Page Count not qualified for processing!")
    return False

  # each page for loop
  log_out(1, "Requesting pages.")
  res_usr_inf = []
  for i in range(whole_page_count):
    current_url = get_current_url(i)
    log_out(2, "Requesting page: " + str(i + 1))
    c_pg = request_json(current_url)
    if check_success(3, c_pg, "Request page") == False:
      return False
    c_rpls = c_pg['data']['replies']
    for rpl in c_rpls:
      def get_usr_inf(rpl):
        try:
          rp_msg = rpl['content']['message']
          mid = rpl['member']['mid']
          uname = rpl['member']['uname']
          sex = rpl['member']['sex']
          avatar = rpl['member']['avatar']
          c_user_inf = {
            'rp_msg': rp_msg,
            'mid': mid,
            'uname': uname,
            'sex': sex,
            'avatar': avatar
          }
          sub_replies = rpl['replies']
          if sub_replies == None or len(sub_replies) == 0:
            c_user_inf.update({
              'replies': []
            })
          else:
            res_sub_rpls = []
            for sub_rpl in sub_replies:
              c_s_rpl = get_usr_inf(sub_rpl)
              res_sub_rpls.append(c_s_rpl)
            c_user_inf.update({
              'replies': res_sub_rpls
            })
          return c_user_inf
        except:
          return None
      c_user_inf = get_usr_inf(rpl)
      if check_success(4, c_user_inf, "Reply Fetch") == False:
        return False
      res_usr_inf.append(c_user_inf)

  log_out(1, "Dumping to json.")
  def opt_json(res_usr_inf):
    res = outptjson(res_usr_inf, "./", "result.json")
    if res == False:
      return None
    else:
      return True
  if check_success(2, opt_json(res_usr_inf), "Dumping to json") == False:
    return

if __name__ == '__main__':
  main_func()
