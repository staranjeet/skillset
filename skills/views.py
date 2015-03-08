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
	if request.POST:
		skill=request.POST['skill'].title()
		score=float(request.POST['score'])
		s=Skils.objects.all()
		if not s:		#means this is the first entry
			newskill=Skils(skill=skill,score=score,normalized=100.0,sessionid=request.session['userId'])
			newskill.save()
		else:
			#now add the scores
			temp=0.0
			for i in s:
				temp=temp+i.score
			#now add the current score
			temp=temp+score
			current_norm_score=(score*100.0)/temp
			newskill=Skils(skill=skill,score=score,normalized=current_norm_score,sessionid=request.session['userId'])
			newskill.save()
			#now update all the skills of this user
			his_skill=Skils.objects.filter(sessionid=request.session['userId'])
			for each_skill in his_skill:
				each_skill.normalized=(each_skill.score*100.0)/temp
				each_skill.save()
		return HttpResponseRedirect('/')
		
	return render_to_response('newskill.html',{'skills':all_skills},context_instance=RequestContext(request))