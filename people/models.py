import uuid

from django.conf import settings
from django.db import models
from lib.image import UploadToDirUUID, UploadToDir, update_image_field

class Language(models.Model):
	name = models.CharField(max_length = 100)
	short = models.CharField(max_length = 100)

	class Meta: ordering = ['name']

	def __str__(self): return '%s' % (self.name)

class Programme(models.Model):
	name = models.CharField(max_length=100)
	shortening = models.CharField(max_length = 100, null = True, blank = True)

	class Meta: ordering = ['name']

	def __str__(self): return '%s' % (self.name)

class Profile(models.Model):
	SHIRT_SIZES = (
		('WXS', 'Woman X-Small'),
		('WS', 'Woman Small'),
		('WM', 'Woman Medium'),
		('WL', 'Woman Large'),
		('WXL', 'Woman X-Large'),
		('MXS', 'Man X-Small'),
		('MS', 'Man Small'),
		('MM', 'Man Medium'),
		('ML', 'Man Large'),
		('MXL', 'Man X-Large'),
	)

	GENDERS = (
		('male', 'Male'),
		('female', 'Female'),
		('other', 'Other')
	)

	user = models.OneToOneField(settings.AUTH_USER_MODEL, default = -1, primary_key = True, on_delete = models.CASCADE)
	birth_date = models.DateField(null=True, blank=True)
	gender = models.CharField(max_length=10, choices=GENDERS, blank=True)
	shirt_size = models.CharField(max_length=3, choices=SHIRT_SIZES, blank=True)
	phone_number = models.CharField(max_length=15, null=True, blank=True)
	drivers_license = models.CharField(max_length=10, null=True, blank=True)
	allergy = models.CharField(max_length=30, null=True, blank=True)
	programme = models.ForeignKey(Programme, null=True, blank=True, on_delete=models.CASCADE)
	registration_year = models.IntegerField(null=True, blank=True)
	planned_graduation = models.IntegerField(null=True, blank=True)
	linkedin_url = models.URLField(null=True, blank=True)
	token = models.CharField(max_length = 255, null = True, blank = False, default = uuid.uuid4)
	slack_id = models.CharField(max_length = 255, null = True, blank = True)
	preferred_language = models.ForeignKey(Language, null = True, blank = True, on_delete = models.CASCADE)
	
	picture_original = models.ImageField(upload_to=UploadToDirUUID('profiles', 'picture_original'), blank = True)
	picture = models.ImageField(upload_to=UploadToDir('profiles', 'picture'), blank = True)
	
	def __str__(self):
		return '%s' % (self.user.get_full_name())
	
	class Meta:
		db_table = 'profile'
		permissions = (('base', 'People'),)
