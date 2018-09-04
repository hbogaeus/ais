from django.db import models
from django.contrib.auth.models import User

from accounting.models import Product
from fair.models import Fair


class Event(models.Model):
	fair = models.ForeignKey(Fair, on_delete = models.CASCADE)
	name = models.CharField(max_length = 75, blank = False, null = False)
	description = models.TextField(blank = True, null = True)
	date_start = models.DateTimeField()
	date_end = models.DateTimeField()
	location = models.CharField(max_length = 75, blank = True, null = True)
	signup_cr = models.BooleanField(blank = False, null = False, verbose_name = 'Let company representatives sign up')
	signup_s = models.BooleanField(blank = False, null = False, verbose_name = 'Let students sign up')
	company_product = models.ForeignKey(Product, null = True, blank = True, on_delete = models.CASCADE, verbose_name = 'Product to link the event with')
	teams_create_cr = models.BooleanField(blank = False, null = False, verbose_name = 'Let company representatives create teams')
	teams_create_s = models.BooleanField(blank = False, null = False, verbose_name = 'Let students create teams')
	teams_participate_cr = models.BooleanField(blank = False, null = False, verbose_name = 'Let company representatives join or leave teams')
	teams_participate_s = models.BooleanField(blank = False, null = False, verbose_name = 'Let students join or leave teams')
	teams_default_max_capacity = models.PositiveIntegerField(blank = True, null = True, verbose_name = 'Default max number of team members') # None => no limit
	fee_s = models.PositiveIntegerField(default = 0, blank = False, null = False, verbose_name = 'Sign-up fee for students')
	published = models.BooleanField(blank = False, null = False, verbose_name = 'The event is published on the website')
	requires_invitation = models.BooleanField(blank = False, null = False, verbose_name = 'Participants need an invitation to sign up')
	contact_person = models.ForeignKey(User, blank = True, null = True, on_delete = models.CASCADE)
	external_event_link = models.CharField(max_length = 255, blank = True, null = True)


class Invitation(models.Model):
	event = models.ForeignKey(Event, on_delete = models.CASCADE)
	invitee = models.ForeignKey(User, blank = True, null = True, on_delete = models.CASCADE)
	fee = models.PositiveIntegerField(blank = True, null = True, verbose_name = 'Fee to participate') # None => default student fee (Event.fee_s)
	date = models.DateTimeField(auto_now_add = True)


class Team(models.Model):
	event = models.ForeignKey(Event, on_delete = models.CASCADE)
	name = models.CharField(max_length = 75, blank = False, null = False)
	leader = models.ForeignKey(User, blank = True, null = True, on_delete = models.CASCADE) # None if a team is created by an administrator
	max_capacity = models.PositiveIntegerField(blank = True, null = True, verbose_name = 'Max number of team members') # None => no limit
	allow_join_cr = models.BooleanField(default = True, blank = False, null = False, verbose_name = 'Allow company representatives to join the team')
	allow_join_s = models.BooleanField(default = True, blank = False, null = False, verbose_name = 'Allow students to join the team')


class Participant(models.Model):
	event = models.ForeignKey(Event, blank = False, null = True, on_delete = models.CASCADE)
	name = models.TextField(blank = True, null = True) # None for students, required for company representatives
	email_address = models.TextField(blank = True, null = True) # None for students, required for company representatives
	phone_number = models.TextField(blank = True, null = True) # None for students, required for company representatives
	user_cr = models.ForeignKey(User, blank = True, null = True, on_delete = models.CASCADE, related_name = 'user_cr') # either this one...
	user_s = models.ForeignKey(User, blank = True, null = True, on_delete = models.CASCADE, related_name = 'user_s')   # ...or this one


class TeamMember(models.Model):
	team = models.ForeignKey(Team, blank = False, null = False, on_delete = models.CASCADE)
	participant = models.ForeignKey(Participant, blank = False, null = False, on_delete = models.CASCADE)


class TeamInvitation(models.Model):
	team = models.ForeignKey(Team, blank = False, null = False, on_delete = models.CASCADE)
	invitee = models.ForeignKey(User, blank = True, null = True, on_delete = models.CASCADE)
	date = models.DateTimeField(auto_now_add = True)
