from django.shortcuts import render
from .models import Post
from django.shortcuts import get_object_or_404

def post(request):
	obj = get_object_or_404(Post, id=1000000)
	context = {
		"instance": obj,
	}
	return render(request, 'whatever.html', context)