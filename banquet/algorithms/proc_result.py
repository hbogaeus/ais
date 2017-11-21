from django.contrib.auth.models import User

from fair.models import Fair
from exhibitors.models import Exhibitor
from people.models import Programme, Profile
from banquet.models import BanquetTable, BanquetTicket, BanquetteAttendant

import pickle
import math
from collections import Counter
import numpy as np


def load_reversed_dict(fname):
    with open(fname, 'rb') as FILE:
        return pickle.load(FILE)

def read_results(fname, ex_dict, stud_dict, tab_dict, var='---- VAR x'):
    data = []
    wFlag = 0
    readidx = 0
    with open(fname, 'r') as FILE:
        lines = FILE.read().splitlines()
    for i in range(len(lines)):
        if lines[i].startswith(var):
            wFlag = 1
            readidx = i

        if wFlag == 1 and i > 3+readidx:
            if lines[i].startswith('---- VAR'):
                wFlag = 0

            if wFlag == 1 and lines[i].startswith('k'):
                line_split = lines[i].split()
                if len(line_split) == 5:
                    if line_split[2] != '.':
                        pass
                        #print(line_split)
                if len(line_split) == 6:
                    if line_split[3] != '.':
                        if line_split[2].startswith('1'):
                            tab_val = int(line_split[0].strip('.').strip(' ').strip('k'))
                            att_val = int(line_split[1].strip('.').strip(' ').strip('j'))
                            try:
                                attendant_id = ex_dict[att_val]
                            except:
                                attendant_id = stud_dict[att_val]
                            tab_id = tab_dict[tab_val]
                            ba = BanquetteAttendant.objects.get(pk=attendant_id)
                            print('%s : %s'%(ba, ba.table.table_name))


def main_process(fair, result_path = 'banquet/algorithms/NEOS_result.html'):
    table_path = 'banquet/algorithms/tables.pkl'
    exhibitor_path = 'banquet/algorithms/exhibitors.pkl'
    student_path = 'banquet/algorithms/students.pkl'
    interest_path = 'banquet/algorithms/interests.pkl'

    table_dict = load_reversed_dict(table_path)
    exhibitor_dict = load_reversed_dict(exhibitor_path)
    student_dict = load_reversed_dict(student_path)
    interest_dict = load_reversed_dict(interest_path)
    read_results(result_path, exhibitor_dict, student_dict, interest_dict)
