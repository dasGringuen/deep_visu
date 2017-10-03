import os
import time
import datetime
import pandas as pd

def seconds2hours(seconds):
	return str(datetime.timedelta(seconds=seconds))

def get_base_name(file):
	full_name = get_normalize_full_path(file)
	return os.path.basename(full_name)

def get_base_name_without_extension(file):
	full_name = get_normalize_full_path(file)
	return os.path.basename(full_name).split(".")[0]

def get_normalize_full_path(path):
    return os.path.abspath(path)

def create_path(out_path):
    o = get_normalize_full_path(out_path)
    retvalue = os.system("mkdir -p " + o)
    print("## Creating path", o)

def get_date_time_string():
    s = datetime.datetime.strftime(datetime.datetime.now(), '%Y.%m.%d-%H.%M.%S.%f')
    return s

def get_date_short():
    s = datetime.datetime.strftime(datetime.datetime.now(), '%Y.%m.%d')
    return s