###########################################################
#
#   Optimization solver for banquet placement
#   =========================================
#   Dependencies:
#       numpy
#       cvxopt
#
#   install these using the ais/requirements_local.txt if
#   you are on a local machine
#   otherwise the requirements.txt should be installed on
#   the ais.
#
###########################################################

from django.contrib.auth.models import User

from fair.models import Fair
from exhibitors.models import Exhibitor
from people.models import Programme, Profile
from banquet.models import BanquetTable, BanquetTicket, BanquetteAttendant

import math
import numpy as np
import cvxopt
from cvxopt import glpk

from . import gams_generator as gen

# The following models are only used locally for the solver
class Attendant(object):

    def get_attendant(self):
        return BanquetteAttendant.objects.get(pk=self.id)

    def __str__(self):
        attendant = BanquetteAttendant.objects.get(pk=self.id)
        return '%i : %s %s'%(self.id, attendant.first_name, attendant.last_name)

class StudentAttendant(Attendant):
    def __init__(self, id, programme_id, gender=2):
        self.id = id
        self.programme_id = programme_id
        self.gender = gender

class ExhibitorAttendant(Attendant):
    def __init__(self, id, programme_id = [], gender = 2):
        self.id = id
        self.programme_id = programme_id
        self.gender = gender

class StaticStudent(Attendant):
    def __init__(self, id, table_id):
        self.id = id
        self.table_id = table_id

class StaticExhibitor(Attendant):
    def __init__(self, id, table_id):
        self.id = id
        self.table_id = table_id

class Table(object):
    def __init__(self, id, number_of_seats):
        self.id = id
        self.number_of_seats = number_of_seats
        self.free_seats = number_of_seats
        self.seated = []

    def put(self, attendant):
        if self.free_seats == 0:
            raise ValueError('Your table is full!')
        else:
            self.seated.append(attendant)
            self.free_seats -= 1

    def __str__(self):
        table = BanquetTable.objects.get(pk=self.id)
        return '%s'%table.table_name

class Interest(object):
    def __init__(self, id):
        self.id = id

    def __str__(self):
        return Programme.objects.get(self.id)

def process_attendants(fair):
    '''
    will return lists of objects for the different types of attendants
Attendant
    students - students which has a programme connected to them and are not ignored from placement

    exhibitors - exhibitors which are not ignored from placement

    statics - all attendants that are ignored from placement

    slacks - any user that is not an exhibitor, not ignored from placement and does not have any kth programme connected to them
    '''
    students = []
    students_static = []
    exhibitors = []
    exhibitors_static = []

    ticket_types = BanquetTicket.objects.all()
    attendants_all = BanquetteAttendant.objects.filter(fair=fair)

    exhibitors_all = [a for a in attendants_all if a.exhibitor]
    for e in exhibitors_all:
        interests = []
        if e.exhibitor.company.related_programme.all():
            interests = [programme.pk for programme in e.exhibitor.company.related_programme.all()]

        exhibitors.append(ExhibitorAttendant(e.pk, interests))
        if e.ignore_from_placement:
            exhibitors_static.append(StaticExhibitor(e.pk, e.table.pk))

    students_all = [a for a in attendants_all if not a.exhibitor]
    for s in students_all:
        programme_id = None
        try:
            user = User.objects.get(pk=s.user.pk)
            user_profile = Profile.objects.get(user=user)
            if user_profile.programme:
                programme_id = user_profile.programme.pk
                print(programme_id)
            else:
                pass
        except:
            pass

        students.append(StudentAttendant(s.pk, programme_id))
        if s.ignore_from_placement:
            students_static.append(StaticStudent(s.pk, s.table.pk))

    tot_length = len(students) + len(exhibitors)
    print('Processing of attendants = %s (#=%i), static exhibitors = %i, static students+rest = %i '%(str(tot_length == len(attendants_all)),len(attendants_all), len(exhibitors_static), len(students_static)))
    return( exhibitors, students, exhibitors_static, students_static, tot_length)

def gen_new_tables(fair, number_of_attendants, size_of_table=8):
    '''
    returns a list ob Table objects of all tables in ais and new ones
    '''
    nr_of_tables = math.ceil(float(number_of_attendants) / float(size_of_table))
    table_numbers = list(np.arange(1,nr_of_tables+1))
    tables_current = BanquetTable.objects.filter(fair=fair)
    current_table_numbers = [int(t.table_name.split(';')[0]) for t in tables_current]
    tables_all = []
    for t in tables_current:
        tables_all.append(Table(t.pk, size_of_table))

    new_table_numbers = [val for val in table_numbers if val not in current_table_numbers]
    for val in new_table_numbers:
        table = BanquetTable.objects.create(
            fair = fair,
            table_name = '%i; Banquet table (autogenerated table!)'%val,
            number_of_seats = size_of_table )
        tables_all.append(Table(table.pk, size_of_table))

    return tables_all

def gen_interest_matrix(rowobjs, colobjs, row_dict, col_dict, offset=0):
    '''
    generates the interest matrices for students and exhibitors
    '''
    matrix = np.zeros((len(rowobjs), len(colobjs)))
    for i, c in enumerate(colobjs):
        if c.programme_id:
            if type(c.programme_id) == list:
                for interest_id in c.programme_id:
                    matrix[row_dict[interest_id]][col_dict[c.id]-offset] = 1
            else:
                matrix[row_dict[c.programme_id]][col_dict[c.id]-offset] = 1
    return(matrix)

def gen_static_matrix(rowobjs, colobjs, row_dict, col_dict, offset=0):
    '''
    generates the static matrices for students and exhibitors
    '''
    matrix = np.zeros((len(row_dict.values()), len(col_dict.values())))
    for i, c in enumerate(colobjs):
        if c.table_id:
            matrix[row_dict[c.table_id]][col_dict[c.id]-offset] = 1
    return(matrix)

def main_process(fair):
    '''
    '''
    (exhibitors, students, exhibitors_static, students_static, tot_length) = process_attendants(fair)
    tables = gen_new_tables(fair, tot_length, 8)
    tables_keys = [t.id for t in tables]
    tables_vals = list(np.arange(len(tables_keys)))
    table_idx_dict = dict(zip(tables_keys, tables_vals))

    # put statics last in lists
    for i in range(len(exhibitors)):
        if exhibitors[i].id in [e.id for e in exhibitors_static]:
            ex_to_move = exhibitors.pop(i)
            exhibitors.append(ex_to_move)
    for i in range(len(students)):
        if students[i].id in [s.id for s in students_static]:
            stud_to_move = students.pop(i)
            students.append(stud_to_move)

    ex_len = len(exhibitors)
    exhibitors_keys = [e.id for e in exhibitors]
    students_keys = [s.id for s in students]
    exhibitors_vals = list(np.arange(ex_len))
    students_vals = list(np.arange(ex_len, ex_len+len(students)))

    exhibitor_idx_dict = dict(zip(exhibitors_keys, exhibitors_vals))
    student_idx_dict = dict(zip(students_keys, students_vals))

    interests = [Interest(p.pk) for p in Programme.objects.all()]
    interests_vals = list(np.arange(len(interests)))
    interests_keys = [i.id for i in interests]
    interest_idx_dict = dict(zip(interests_keys, interests_vals))

    ex_interest_mat = gen_interest_matrix(interests, exhibitors, interest_idx_dict, exhibitor_idx_dict)
    stud_interest_mat = gen_interest_matrix(interests, students, interest_idx_dict, student_idx_dict, len(exhibitors))

    ex_static_mat = gen_static_matrix(tables, exhibitors_static, table_idx_dict, exhibitor_idx_dict)
    stud_static_mat = gen_static_matrix(tables, students_static, table_idx_dict, student_idx_dict, len(exhibitors))

    print(stud_static_mat.sum(axis=1))



def solver(fair):
    '''
    '''
    main_process(fair)
    #outfile_path = 'banquet/algorithms/test.gms'
    #eqnfile_path = 'banquet/algorithms/opt_eqn_banquet.gms'
    '''
    with open(outfile_path, 'w+') as FILE:
        tot_attendants = 10
        tot_tables = 5
        tot_interests = 5
        exhibitors_idx = [1,5]
        students_idx = [6,10]
        static_ex = [3,5]
        static_stud = [8,10]
        gen.gen_init_strings(FILE, tot_attendants, tot_tables, tot_interests, exhibitors_idx, students_idx, static_ex, static_stud)
        gen.gen_gams_eqns(FILE, eqnfile_path)
    '''



#fair = Fair.objects.get(current=True)
#solver(fair)
