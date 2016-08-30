from django.shortcuts import render, redirect, HttpResponse
from . import models
from models import User, Appointment
import datetime

# Create your views here.
def index(request):
	request.session.pop('id', None)
	# request.session.pop('errors', None)
	# request.session.pop('login_errors', None)
	# request.session.pop('name', None)
	return render(request, 'appointments/index.html')

def register(request):
	name = request.POST['name']
	email = request.POST['email']
	password = request.POST['password']
	confirmPW = request.POST['confirmPW']
	dob = request.POST['dob']
	result = User.userMgr.validateRegis(name=name, email=email, password=password, confirmPW=confirmPW, dob=dob)
	if result[0]:
		request.session['name'] = name
		request.session.pop('errors', None)
		return redirect('/')
	else:
		request.session['errors'] = result[1]
		return redirect('/')

def login(request):
	login_email = request.POST['login_email']
	login_pw = request.POST['login_pw']
	result = User.userMgr.validateLogin(login_email=login_email, login_pw=login_pw)
	if result[0]:
		request.session.pop('name', None)
		getUser = result[1]
		request.session['id'] = getUser.id
		request.session['name'] = getUser.name
		request.session.pop('login_errors', None)
		return redirect('/appointments')
	else:
		request.session['login_errors'] = result[1]
		return redirect('/')

def showDashboard(request):
	today = datetime.date.today()
	today = str(today)
	todays_appts = models.Appointment.objects.filter(user=request.session['id']).filter(date=today).values('task', 'time', 'status', 'date', 'id').order_by('time')
	future_appts = models.Appointment.objects.filter(user=request.session['id']).filter(date__gt=today).values('task', 'time', 'status', 'date', 'id').order_by('date', 'time')
	context = {'todays_appts':todays_appts, 'future_appts':future_appts, 'today':today}
	return render(request, 'appointments/dashboard.html', context)

def create(request):
	userID = request.session['id']
	appt_date = request.POST['appt_date']
	appt_time = request.POST['appt_time']
	appt_tasks = request.POST['appt_tasks']
	result = User.userMgr.createAppt(appt_date=appt_date, appt_time=appt_time, appt_tasks=appt_tasks, id=userID)
	if result[0]:
		getTask = result[1].task
		request.session.pop('task', None)
		request.session.pop('addappt_errors', None)
		request.session['task'] = getTask
		return redirect('/appointments')
	else:
		request.session['addappt_errors'] = result[1]
		return redirect('/appointments')

def editAppt(request, id):
	request.session.pop('task', None)
	getAppt = models.Appointment.objects.get(pk=id)
	convertTime = str(getAppt.time)
	convertTime = datetime.datetime.strptime(convertTime, '%H:%M:%S').strftime('%I:%M:%S')
	context = {'getAppt':getAppt, 'convertTime':convertTime}
	return render(request, 'appointments/editappt.html', context)

def updateAppt(request, id):
	update_task = request.POST['update_task']
	update_status = request.POST['update_status']
	update_date = request.POST['update_date']
	update_time = request.POST['update_time']
	appt_id = id
	result = User.userMgr.updateAppt(update_task=update_task, update_date=update_date, update_time=update_time, update_status=update_status, id=appt_id)
	if result[0]:
		request.session.pop('update_errors', None)
		return redirect('/appointments')
	else:
		request.session['update_errors'] = result[1]
		return redirect('/appointments/'+id)

def deleteAppt(request, id):
	appt = models.Appointment.objects.get(pk=id).delete()
	return redirect('/appointments')

def logout(request):
	request.session.pop('errors', None)
	request.session.pop('name', None)
	request.session.pop('login_errors', None)
	request.session.pop('id', None)
	request.session.pop('addappt_errors', None)
	request.session.pop('task', None)
	request.session.pop('update_errors', None)
	return redirect('/')