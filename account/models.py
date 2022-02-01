from inspect import modulesbyfile
from django.core.validators import MaxValueValidator, MinValueValidator

from unicodedata import category
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
import uuid


class MyAccountManager(BaseUserManager):
	def create_user(self, email, username, password=None):
		if not email:
			raise ValueError('Users must have an email address')
		if not username:
			raise ValueError('Users must have a username')

		user = self.model(
			email=self.normalize_email(email),
			username=username,
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username, password):
		user = self.create_user(
			email=self.normalize_email(email),
			password=password,
			username=username,
		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user


def get_profile_image_filepath(self, filename):
	return 'profile_images/' + str(self.pk) + '/profile_image.png'

def get_default_profile_image():
	return "codingwithmitch/logo_1080_1080.png"

DEFAULT_RATING = 50
MAX_RATING = 100
MIN_RATING = 0

class Account(AbstractBaseUser):
	email 					= models.EmailField(verbose_name="email", max_length=60, unique=True)
	username 				= models.CharField(max_length=100, unique=True)
	parent					= models.CharField(max_length=100, null=True, blank=True)
	dt_ob             		= models.DateField(verbose_name='date of birth', null=True, blank=True)
	CAST_CHOICES= (
 		 (None, 'Select'),
         ('cast-1', 'SC'),
         ('cast-2', 'ST'),
         ('cast-3', 'OBC-A'),
         ('cast-4', 'OBC-B'),
         ('cast-5', 'GEN'),
	)
	catg                    = models.CharField(verbose_name='Category',max_length=6, choices=CAST_CHOICES, null=True, blank=True)
	Department              = models.ForeignKey("Department", on_delete=models.CASCADE, null=True, blank=True)
	current_dsg				= models.CharField(verbose_name='Present Dsgn.',max_length=30, null=True, blank=True)
	AGP_CHOICES= (
 		 (None, 'Select'),
         (1, '6000'),
         (2, '7000'),
         (3, '8000'),
         (4, '9000'),
         (5, '10000'),         
	)
	agp						= models.IntegerField(verbose_name='AGP fig.',choices=AGP_CHOICES, null=True)
	dt_last_promo			= models.DateField(verbose_name='Date of last promotion',null=True)
	dt_eligibility			= models.DateField(verbose_name='Date of promo elig',)
	addr_corres             = models.TextField(verbose_name='Address for corres',max_length=300,null=True,blank=True)
	addr_perm               = models.TextField(verbose_name='Address for permanent',max_length=300,null=True,blank=True)
	mobile                  = models.CharField(default="Individual", max_length=10,null=True,blank=True)
	date_joined				= models.DateField(verbose_name='Date of joining',null=True)
	last_login				= models.DateTimeField(verbose_name='last login', auto_now=True)
	is_admin				= models.BooleanField(default=False)
	is_active				= models.BooleanField(default=True)
	is_staff				= models.BooleanField(default=False)
	is_superuser			= models.BooleanField(default=False)
	is_carry				= models.BooleanField(default=False)
	profile_image			= models.ImageField(max_length=255, upload_to=get_profile_image_filepath, null=True, blank=True, default=get_default_profile_image)
	hide_email				= models.BooleanField(default=True)
	
	DSG_CHOICES = (
 		 (None, 'Select'),
         ('dsg-1', 'Assistant Professor'),
         ('dsg-2', 'Associate Professor'),
	)
	Designation             = models.CharField(max_length=30, choices=DSG_CHOICES, null=True, blank=True)
	highest_quali			= models.CharField(max_length=200, null=True, blank=True)
	pan_no					= models.CharField(max_length=10, null=True, blank=True)
	GENDER_CHOICES = (
     	(None, 'Select'),       
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
	gender					= models.CharField(verbose_name='Gender(M/F)',max_length=6, choices=GENDER_CHOICES, null=True, blank=True)
	quali_year				= models.CharField(verbose_name='Qualifying Year',max_length=4, null=True, blank=True)
	dt_ob             		= models.DateField(verbose_name='date of birth', null=True, blank=True)
	tot_experience			= models.IntegerField(verbose_name='Total Experience in year', default=0)
	POST_CHOICES = (
     	(None, 'Select Posts'),
        ('Stage 2', 'Assistant Prof. (Stage 2)'),
        ('Stage 3', 'Assistant Prof. (Stage 3)'),
        ('Stage 4', 'Associate Prof. (Stage 4)'),
        ('Stage 5', 'Professor (Stage 5)')
    )
	post					= models.CharField(verbose_name='Post applied for',max_length=30,choices=POST_CHOICES,null=True, blank=True)
	FROM_CHOICES = (
     	(None, 'Select Posts'),
        ('Stage 1', 'Assistant Prof. (Stage 1)'),
        ('Stage 2', 'Assistant Prof. (Stage 2)'),
        ('Stage 3', 'Assistant Prof. (Stage 3)'),
        ('Stage 4', 'Associate Prof. (Stage 4)')
    )
	from_dsg                = models.CharField(verbose_name='From stage/desgn.',max_length=30,choices=FROM_CHOICES,null=True, blank=True)
	TO_CHOICES = (
     	(None, 'Select Posts'),
        ('Stage 2', 'Assistant Prof. (Stage 2)'),
        ('Stage 3', 'Assistant Prof. (Stage 3)'),
        ('Stage 4', 'Associate Prof. (Stage 4)'),
        ('Stage 5', 'Professor (Stage 5)')
    )
	to_dsg                  = models.CharField(verbose_name='To stage/desgn.',max_length=30,choices=TO_CHOICES,null=True, blank=True)
 
 
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username']

	objects = MyAccountManager()

	def __str__(self):
		return self.username

	def get_profile_image_filename(self):
		return str(self.profile_image)[str(self.profile_image).index('profile_images/' + str(self.pk) + "/"):]

	# For checking permissions. to keep it simple all admin have ALL permissons
	def has_perm(self, perm, obj=None):
		return self.is_admin

	# Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
	def has_module_perms(self, app_label):
		return True

class Department(models.Model):
    name = models.CharField(max_length=200, unique=True)
 
    def __str__(self):
        return self.name

 
  
    