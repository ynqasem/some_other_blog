from django.shortcuts import render
from django.http import JsonResponse
import requests

def text_search(request):
	api_key = "AIzaSyALU-dHI46zRtxOcr18gWDyJ3Kh9zXGBps"
	query = request.GET.get("query", '')
	next_page_token = request.GET.get("next_page_token")
	url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?query='+query+'&key='+api_key
	if next_page_token is not None:
		url+="&pagetoken=%s"%(next_page_token)
	response = requests.get(url)
	return JsonResponse(response.json(), safe=False)
	# return render(request, 'text.html', {'response': response.json()})

def place_detail(request):
	api_key = "AIzaSyALU-dHI46zRtxOcr18gWDyJ3Kh9zXGBps"
	key = 'AIzaSyA8CthEZDzsjWGTIHHkta9Rgvs-VF4rlK4'
	reference = request.GET.get("reference")
	url = 'https://maps.googleapis.com/maps/api/place/details/json?reference=%s&key=%s'%(reference, api_key)
	response = requests.get(url)
	# return JsonResponse(response.json(), safe=False)
	return render(request, 'detail.html', {'response': response.json(), 'key': key})

def radius_search(request):
	api_key = "AIzaSyALU-dHI46zRtxOcr18gWDyJ3Kh9zXGBps"
	location = request.GET.get("location")
	radius = request.GET.get("radius",'')
	url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?key=%s&location=%s&radius=%s'%(api_key, location, radius)
	response = requests.get(url)
	# return JsonResponse(response.json(), safe=False)
	return render(request, 'radius.html', {'response': response.json()})