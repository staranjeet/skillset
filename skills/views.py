from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from skills.models import *
from django.core.context_processors import csrf
from django.template import RequestContext

# Create your views here.

def index(request):
	return render_to_response('index.html')

def allskill(request):
	if 'userId' not in request.session:
		#print 'user at new loc page'
		if not request.session.exists(request.session.session_key):
			print 'checking and creating a new session'
			request.session.create()
		request.session['userId']=request.session._session_key
	all_skills=Skils.objects.filter(sessionid=request.session['userId'])
	return render_to_response('allskill.html',{'skills':all_skills})

def newskill(request):
	c = {}
	c.update(csrf(request))
	all_skills=None
	if 'userId' not in request.session:
		#print 'user at new loc page'
		if not request.session.exists(request.session.session_key):
			print 'checking and creating a new session'
			request.session.create()
		request.session['userId']=request.session._session_key
	session_id=request.session['userId']
	if request.POST:
		skill=request.POST['skill'].title()
		score=float(request.POST['score'])
		s=Skils.objects.filter(sessionid=session_id)
		if not s:		#means this is the first entry
			newskill=Skils(skill=skill,score=score,normalized=100.0,sessionid=session_id)
			newskill.save()
		else:
			#now add the scores
			temp=0.0
			for i in s:
				temp=temp+i.score
			#now add the current score
			temp=temp+score
			current_norm_score=(score*100.0)/temp
			newskill=Skils(skill=skill,score=score,normalized=current_norm_score,sessionid=session_id)
			newskill.save()
			#now update all the skills of this user
			his_skill=Skils.objects.filter(sessionid=session_id)
			for each_skill in his_skill:
				each_skill.normalized=(each_skill.score*100.0)/temp
				each_skill.save()
		return HttpResponseRedirect('/')
	all_skills=Skils.objects.filter(sessionid=request.session['userId'])	
	return render_to_response('newskill.html',{'skills':all_skills},context_instance=RequestContext(request))

def deleteskill(request):
	if request.GET:
		session_id=request.session['userId']
		skill=request.GET['sname']
		all_skills=Skils.objects.filter(sessionid=session_id)
		temp=0.0
		for i in all_skills:
			temp = temp + i.score
		s=Skils.objects.filter(sessionid=session_id,skill=skill)

		#delete the current score
		for i in s:
			temp = temp - i.score
			i.delete()

		#update the normalized scores again
		his_skill=Skils.objects.filter(sessionid=session_id)
		for each_skill in his_skill:
			each_skill.normalized=(each_skill.score*100.0)/temp
			each_skill.save()

		#return HttpResponse('/allskill')
	return HttpResponseRedirect('/newskill')