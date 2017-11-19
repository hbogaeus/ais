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

# The following models are only used locally for the solver
class Attendant(object):
    def __str__(self):
        attendant = BanquetteAttendant.objects.get(pk=self.id)
        return '%i : %s %s'%(self.id, attendant.first_name, attendant.last_name)

class StudentAttendant(Attendant):
    def __init__(self, id, programme_id):
        self.id = id
        self.programme_id = programme_id

class ExhibitorAttendant(Attendant):
    def __init__(self, id, interest_ids = []):
        self.id = id
        self.interest_ids = interest_ids

class SlackAttendant(Attendant):
    def __init__(self, id):
        self.id = id

class StaticAttendant(Attendant):
    def __init__(self, id):
        self.id = id

class Table(object):
    def __init__(self, id, number_of_seats):
        self.id = id
        self.number_of_seats = number_of_seats
        self.free_seats = number_of_seats
        self.seated = []

    def put_static(self, attendant):
        if self.free_seats == 0:
            raise ValueError('Your table is full!')
        else:
            self.seated.append(attendant)
            self.free_seats -= 1

    def __str__(self):
        table = BanquetTable.objects.get(self.id)
        return '%s'%table.table_name

def process_attendants(fair):
    '''
    will return lists of objects for the different types of attendants

    students - students which has a programme connected to them and are not ignored from placement

    exhibitors - exhibitors which are not ignored from placement

    statics - all attendants that are ignored from placement

    slacks - any user that is not an exhibitor, not ignored from placement and does not have any kth programme connected to them
    '''
    students = []
    statics = []
    slacks = []
    exhibitors = []

    ticket_types = BanquetTicket.objects.all()
    attendants_all = BanquetteAttendant.objects.filter(fair=fair)

    exhibitors_all = [a for a in attendants_all if a.exhibitor]
    for e in exhibitors_all:
        interets = []
        if e.exhibitor.company.related_programme.all():
            interests = [programme.pk for programme in e.exhibitor.company.related_programme.all()]
        exhibitors.append(ExhibitorAttendant(e.pk, interests))

    not_exhibitors = [a for a in attendants_all if not a.exhibitor]

    for ne in not_exhibitors:
        if ne.ignore_from_placement:
            statics.append(StaticAttendant(ne.pk))
        else:
            try:
                user = User.objects.get(pk=ne.user.pk)
                user_profile = Profile.objects.get(user=user)
                if user_profile.programme:
                    students.append(StudentAttendant(ne.pk, user_profile.programme.pk))
                else:
                    slacks.append(SlackAttendant(ne.pk))
            except Exception as e:
                print(str(e))
                slacks.append(SlackAttendant(ne.pk))
    tot_length = len(exhibitors) + len(students) + len(statics) + len(slacks)
    print('Processing of attendants = %s (#=%i) '%(str(tot_length == len(attendants_all)),len(attendants_all)))
    return( exhibitors, students, statics, slacks, tot_length )

def process_tables(fair, exhibitors, statics, number_of_attendants):
    '''
    '''
    tables_all = BanquetTable.objects.filter(fair=fair)
    tables = [Table(t.pk, t.number_of_seats) for t in tables_all]
    try:
        for s in statics:
            s = BanquetteAttendant.objects.get(pk=s.id)
            if s.table:
                for t in tables:
                    if s.table.pk == t.id:
                        t.put_static(s)
                        break
    except TypeError as e:
        raise Exception('There is probably some Nonetype in the tables!')

    return tables


def main_process(fair):
    '''
    '''
    (exhibitors, students, statics, slacks, tot_length) = process_attendants(fair)
    initial_tables = process_tables(fair, exhibitors, statics, tot_length)
    for it in initial_tables:
        print(it)
        print(it.number_of_seats)
        print(it.free_seats)
        print('_____________')

def solver(fair):
    '''
    '''
    main_process(fair)

fair = Fair.objects.get(current=True)
solver(fair)
