from django.shortcuts import render, redirect
from .models import Post
from .forms import PostForm
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def post_list(request):
	obj_list = Post.objects.all()#.order_by("-timestamp","-updated")
	paginator = Paginator(obj_list, 10)
	page = request.GET.get('page')
	try:
		objs = paginator.page(page)
	except PageNotAnInteger:
		objs = paginator.page(1)
	except EmptyPage:
		objs = paginator.page(paginator.num_pages)
	context = {
		"post_list": objs,
	}
	return render(request, 'post_list.html', context)


def post_detail(request, post_id):
	obj = get_object_or_404(Post, id=post_id)
	context = {
		"instance": obj,
	}
	return render(request, 'post_detail.html', context)

def post_create(request):
	form = PostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		form.save()
		messages.success(request, "OMG! So cool! You created an object.")
		return redirect("posts:list")
	context = {
		"form":form,
	}
	return render(request, 'post_create.html', context)


def post_update(request, post_id):
	post_object = get_object_or_404(Post, id=post_id)
	form = PostForm(request.POST or None, request.FILES or None, instance=post_object)
	if form.is_valid():
		form.save()
		messages.success(request, "Giving it a second thought?")
		return redirect("posts:list")
	context = {
		"form":form,
		"post_object":post_object,
	}
	return render(request, 'post_update.html', context)


def post_delete(request, post_id):
	Post.objects.get(id=post_id).delete()
	messages.warning(request, "Seriously bro?")
	return redirect("posts:list")
	