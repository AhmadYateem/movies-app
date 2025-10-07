from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .forms import VideoForm
from .models import Video
from django.db.models import Q


def index(request):
	return render(request,'index.html')


def video_list(request):
	search_query = request.GET.get('search', '')
	videos = Video.objects.all()
	
	if search_query:
		videos = videos.filter(
			Q(MovieTitle__icontains=search_query) |
			Q(Actor1Name__icontains=search_query) |
			Q(Actor2Name__icontains=search_query) |
			Q(DirectorName__icontains=search_query) |
			Q(MovieGenre__icontains=search_query)
		)
	
	return render(request, 'video_list.html', {'videos': videos, 'search_query': search_query})


def video_detail(request, pk):
	try:
		video = Video.objects.get(pk=pk)
	except Video.DoesNotExist:
		video = None
	return render(request, 'video_detail.html', {'video': video})


def video_create(request):
	if request.method == 'POST':
		form = VideoForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('video_list')
	else:
		form = VideoForm()
	return render(request, 'video_form.html', {'form': form, 'creating': True})


def video_update(request, pk):
	try:
		video = Video.objects.get(pk=pk)
	except Video.DoesNotExist:
		return redirect('video_list')
	
	if request.method == 'POST':
		form = VideoForm(request.POST, instance=video)
		if form.is_valid():
			form.save()
			return redirect('video_detail', pk=video.MovieID)
	else:
		form = VideoForm(instance=video)
	return render(request, 'video_form.html', {'form': form, 'creating': False, 'video': video})


def video_delete(request, pk):
	try:
		video = Video.objects.get(pk=pk)
	except Video.DoesNotExist:
		return redirect('video_list')
	
	if request.method == 'POST':
		video.delete()
		return redirect('video_list')
	return render(request, 'video_confirm_delete.html', {'video': video})

		