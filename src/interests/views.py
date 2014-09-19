# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render_to_response, RequestContext, Http404, HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Interest, UserInterestAnswer, InterestPicture
from .forms import InterestForm
from django.core.urlresolvers import reverse
from django.core.cache import cache





def create_interest(request):
	form = InterestForm(request.POST or None)
	if form.is_valid():
		interest = form.save(commit=False)
		interest.save()
		messages.success(request, 'Interest Created')
		return HttpResponseRedirect('/interests/')


	return render_to_response("interests/create.html", locals(),
		 context_instance=RequestContext(request))


def all_interests(request):
	if not request.session.get('random_interests'):
		request.session['random_interests']= request.user.id
	interests_all = cache.get('random_interests_%d' % request.session['random_interests'])
	if not interests_all:
		interests_all = list(Interest.objects.exclude(userinterestanswer__user=request.user).filter(approved=True).order_by('?'))
		cache.set('random_interests_%d' % request.session['random_interests'], interests_all, 100)
	#interests_all = Interest.objects.exclude(userinterestanswer__user=request.user).filter(approved=True).order_by('?')
	paginator = Paginator(interests_all, 1)
	importance_levels = ['Strongly Dislike', 'Dislike', 'Neutral', 'Like', 'Strongly Like']

	page = request.GET.get('page')
	print page
	try:
		interests = paginator.page(page)
	except PageNotAnInteger:
		#If page is not an integer, deliver first page.
		interests = paginator.page(1)
	except EmptyPage:
		#If page is out of range, deliver last page of results
		interests = paginator.page(paginator.num_pages)

	if request.method == 'POST':
		interest_id = request.POST['interest_id']

		#user answer
		importance_level = request.POST['importance_level']

		user = User.objects.get(id=request.user.id)
		interest = Interest.objects.get(id=interest_id)
		try:
			interest_pic = InterestPicture.objects.get(interest=interest).filter(id=1)
		except: 
			pass

		#user answer save

		answered, created = UserInterestAnswer.objects.get_or_create(user=user, interest=interest)
		answered.importance_level = importance_level
		answered.save()
		if not request.session.get('random_interests'):
			request.session['random_interests']= request.user.id
		interests_all = list(Interest.objects.exclude(userinterestanswer__user=request.user).filter(approved=True).order_by('?'))
		cache.set('random_interests_%d' % request.session['random_interests'], interests_all, 100)
		paginator = Paginator(interests_all, 1)
		importance_levels = ['Strongly Dislike', 'Dislike', 'Neutral', 'Like', 'Strongly Like']

		page = request.GET.get('page')
	
		try:
			interests = paginator.page(page)
		except PageNotAnInteger:
		#If page is not an integer, deliver first page.
			interests = paginator.page(1)
		except EmptyPage:
		#If page is out of range, deliver last page of results
			interests = paginator.page(paginator.num_pages)


	return render_to_response('interests/all.html', locals(), context_instance=RequestContext(request))


def edit_interests(request):

	interests_all = Interest.objects.filter(userinterestanswer__user=request.user)
	paginator = Paginator(interests_all, 1)
	importance_levels = ['Strongly DisLike', 'DisLike', 'Neutral', 'Like', 'Strongly Like']

	page = request.GET.get('page')
	try:
		interests = paginator.page(page)
	except PageNotAnInteger:
		#If page is not an integer, deliver first page.
		interests = paginator.page(1)
	except EmptyPage:
		#If page is out of range, deliver last page of results
		interets = paginator.page(paginator.num_pages)

	if request.method == 'POST':
		interest_id = request.POST['interest_id']

		#user answer
		importance_level = request.POST['importance_level']

		user = User.objects.get(id=request.user.id)
		interest = Interest.objects.get(id=interest_id)
		try:
			interest_pic = InterestPicture.objects.get(interest=interest).filter(id=1)
		except: 
			pass

		#user answer save

		answered, created = UserInterestAnswer.objects.get_or_create(user=user, interest=interest)
		answered.importance_level = importance_level
		answered.save()

		return HttpResponseRedirect('')
	return render_to_response('interests/edit.html', locals(), context_instance=RequestContext(request))


# displays the interests for a particular user
def single_user_interests(request, username):
	single_user = User.objects.get(username=username)
	interests_all = Interest.objects.filter(userinterestanswer__user=single_user)
	paginator = Paginator(interests_all, 1)
	importance_levels = ['Strongly Dislike', 'Dislike', 'Neutral', 'Like', 'Strongly Like']

	page = request.GET.get('page')
	try:
		interests = paginator.page(page)
	except PageNotAnInteger:
		#If page is not an integer, deliver first page.
		interests = paginator.page(1)
	except EmptyPage:
		#If page is out of range, deliver last page of results
		interets = paginator.page(paginator.num_pages)

	return render_to_response('interests/single_user.html', locals(), context_instance=RequestContext(request))



def new_user_interests(request):
	interests_all = Interest.objects.filter(for_new_users=True)
	paginator = Paginator(interests_all, 1)
	importance_levels = ['Strongly Dislike', 'Dislike', 'Neutral', 'Like', 'Strongly Like']

	page = request.GET.get('page')
	try:
		interests = paginator.page(page)
	except PageNotAnInteger:
		#If page is not an integer, deliver first page.
		interests = paginator.page(1)
	except EmptyPage:
		#If page is out of range, deliver last page of results
		interests = paginator.page(paginator.num_pages)

	if request.method == 'POST':
		interest_id = request.POST['interest_id']

		#user answer

		#user = User.objects.get(id=request.user.id)
		interest = Interest.objects.get(id=interest_id)
		try:
			interest_pic = InterestPicture.objects.get(interest=interest).filter(id=1)
		except: 
			pass

		#user answer save

		answered, created = UserInterestAnswer.objects.get_or_create(user=request.user, interest=interest)
		answered.save()

		interests_all = Interest.objects.filter(for_new_users=True).exclude(userinterestanswer__user=request.user)
		paginator = Paginator(interests_all, 1)
		importance_levels = ['Strongly Dislike', 'Dislike', 'Neutral', 'Like', 'Strongly Like']

		page = request.GET.get('page')
		try:
			interests = paginator.page(page)
		except PageNotAnInteger:
			#If page is not an integer, deliver first page.
			interests = paginator.page(1)
		except EmptyPage:
		#If page is out of range, deliver last page of results
			interests = paginator.page(paginator.num_pages)


		user_interests = UserInterestAnswer.objects.filter(user=request.user)
		if user_interests.count() == 10: 
			return HttpResponseRedirect(reverse('handle_new_user'))

	return render_to_response('interests/new_user.html', locals(), context_instance=RequestContext(request))


