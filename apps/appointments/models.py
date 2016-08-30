from __future__ import unicode_literals
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
import bcrypt
import datetime
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

# Create your models here.
class UserManager(models.Manager):
	def validateRegis(self, **kwargs):
		errors = []
		dob = kwargs['dob']
		dob = datetime.datetime.strptime(dob, '%m/%d/%Y').strftime('%Y-%m-%d')
		if len(kwargs['name']) < 1:
			errors.append('Name cannot be empty')
		if len(kwargs['email']) < 1:
			errors.append('Email cannot be empty')
		if not EMAIL_REGEX.match(kwargs['email']):
			errors.append("Email address is invalid, please try again")
		if len(kwargs['password']) < 1:
			errors.append("Must fill in password")
		if len(kwargs['password']) < 8:
			errors.append("Password must be more than 8 characters")
		if kwargs['password'] != kwargs['confirmPW']:
			errors.append("Password and Password Confirmation do not match")
		if len(dob) < 1:
			errors.append("Must enter Date of Birth")
		if len(errors) > 0:
			return (False, errors)
		else:
			password = kwargs['password']
			password = password.encode()
			pw_hash = bcrypt.hashpw(password, bcrypt.gensalt())
			user = User.userMgr.create(name=kwargs['name'], email=kwargs['email'], pw_hash=pw_hash, dob=dob)
			return (True, user)

	def validateLogin(self, **kwargs):
		pw_hash = User.userMgr.filter(email=kwargs['login_email']).values('pw_hash')
		pw_hash = pw_hash[0].values()
		pw_hash = pw_hash[0].encode()
		user = User.userMgr.get(email=kwargs['login_email'])
		input_password = kwargs['login_pw'].encode()
		try:
			if bcrypt.hashpw(input_password, pw_hash) == pw_hash:
				return (True, user)
		except ObjectDoesNotExist:
			pass
		return (False, ['Email/Password does not match. Please try again.'])

	def createAppt(self, **kwargs):
		errors = []
		appt_date = kwargs['appt_date']
		today = datetime.date.today()
		today = str(today)
		appt_date = datetime.datetime.strptime(appt_date, '%m/%d/%Y').strftime('%Y-%m-%d')
		if len(appt_date) < 1:
			errors.append("Must enter an appointment date")
		if appt_date < today:
			errors.append("Appointment date must be current or future date")
		if len(kwargs['appt_time']) < 1:
			errors.append("Must enter an appointment time")
		if len(kwargs['appt_tasks']) < 1:
			errors.append("Must enter appointment task(s)")
		if len(errors) > 0:
			return (False, errors)
		else:
			getUser = self.get(pk=kwargs['id'])
			new_appt = Appointment.objects.create(date=appt_date, time=kwargs['appt_time'], status="Pending", task=kwargs['appt_tasks'], user=getUser)
			return (True, new_appt)

	def updateAppt(self, **kwargs):
		errors = []
		today = datetime.date.today()
		today = str(today)
		update_date = kwargs['update_date']
		update_date = datetime.datetime.strptime(update_date, '%m/%d/%Y').strftime('%Y-%m-%d')
		if len(kwargs['update_task']) < 1:
			errors.append("Must enter tasks")
		if update_date < 1:
			errors.append("Must enter a date")
		if update_date < today:
			errors.append("Date must be current or future date")
		if len(kwargs['update_time']) < 1:
			errors.append("Must enter a time")
		if len(errors) > 0:
			return (False, errors)
		else:
			updateAppt = Appointment.objects.filter(id=kwargs['id']).update(task=kwargs['update_task'], time=kwargs['update_time'], status=kwargs['update_status'], date=update_date)
			return (True, updateAppt)



class User(models.Model):
	name = models.CharField(max_length=255)
	email = models.EmailField(max_length=255)
	pw_hash = models.CharField(max_length=255)
	dob = models.DateField(auto_now=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	userMgr = UserManager()

class Appointment(models.Model):
	date = models.DateField(auto_now=False)
	time = models.TimeField(auto_now=False)
	status = models.CharField(max_length=10)
	task = models.CharField(max_length=255)
	user = models.ForeignKey(User, related_name="usertoappt")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

