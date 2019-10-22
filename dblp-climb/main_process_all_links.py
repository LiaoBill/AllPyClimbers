import requests
from bs4 import BeautifulSoup

# for time calculation
from time import time
from datetime import datetime

import os

def process_1file(cf):
  try:
    f = open(
      "./dt/" + cf,
      "rt"
    )
    cl = f.readlines()
    f.close()
    cl = [l.strip() for l in cl]
    nl = list(set(cl))
    nl.sort(key=cl.index)
    f = open(
      "./dt/" + cf,
      "wt"
    )
    for cn in nl:
      f.write(cn+"\n")
    f.close()
  except:
    return False
  return True

def main_func():
  fp = "./dt/"
  all_fs = os.listdir(fp)
  for cf in all_fs:
    if process_1file(cf) == False:
      print("ERROR WHEN : -- " + cf)
      break

if __name__ == '__main__':
  main_func()