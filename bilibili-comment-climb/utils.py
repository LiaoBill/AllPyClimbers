import json
import os
from datetime import datetime

lg_file_path = None

def get_abs_fp(path, file_name):
  abs_f_path = ""
  if path.endswith("/"):
    abs_f_path = path + file_name
  else:
    abs_f_path = path + "/" + file_name
  return abs_f_path

def mkfile(path, file_name):
  try:
    os.makedirs(path, exist_ok=True)
  except:
    return False
  abs_f_path = get_abs_fp(path, file_name)
  try:
    f = open(
      abs_f_path,
      "wt",
      encoding="utf-8"
    )
    f.close()
    return True
  except:
    return False

def set_lg_file(path, log_name):
  if mkfile(path, log_name) == True:
    global lg_file_path
    lg_file_path = get_abs_fp(path, log_name)
    return True
  else:
    return False

def write_lg_file(lg_str):
  global lg_file_path
  try:
    f = open(
      lg_file_path,
      "at",
      encoding="utf-8"
    )
    f.write(lg_str + "\n")
    f.close()
    return True
  except:
    return False

def get_lg_content(level, str, tag):
  level_str = "".ljust(level*2, " ") + "* "
  ct = datetime.now()
  t_id = ct.strftime('%Y-%m-%d-%H-%M-%S')
  if tag == "LOG":
    return "[ LOG--" + t_id + "]   : " + level_str + str
  elif tag == "ERROR":
    return "[ ERROR--" + t_id + "] : WHEN  " + level_str + str

def log_out(level, str):
  lg_str =  get_lg_content(level, str, "LOG")
  print(lg_str)
  global lg_file_path
  if lg_file_path == None:
    pass
  else:
    return write_lg_file(lg_str)

def error_out(level, str):
  lg_str =  get_lg_content(level, str, "ERROR")
  print(lg_str)
  global lg_file_path
  if lg_file_path == None:
    pass
  else:
    return write_lg_file(lg_str)

def outptjson(js_data, file_path, file_name):
  jsonstr = json.dumps(js_data, indent=2, ensure_ascii=False)
  if mkfile(file_path, file_name) == True:
    abs_f_path = ""
    if file_path.endswith("/"):
      abs_f_path = file_path + file_name
    else:
      abs_f_path = file_path + "/" + file_name
    f = open(
      abs_f_path,
      "wt",
      encoding="utf-8"
    )
    f.write(jsonstr)
    f.close()
    return True
  else:
    return False

def readjson(file_path, file_name):
  abs_fp = get_abs_fp(file_path, file_name)
  if os.path.exists(abs_fp) == True:
    try:
      f = open(
        abs_fp,
        "r",
        encoding='utf-8'
      )
      jsonstr = f.read(-1)
      dt = json.loads(jsonstr)
      f.close()
      return dt
    except:
      return None
  else:
    return None
