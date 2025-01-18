from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.core import serializers
from django.http import HttpResponse
from django.utils import timezone
from .forms import PostCreateForm

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

def posts(request):
    posts = Post.objects.filter(published_at__isnull=False).order_by('-published_at')
    return render(request, 'blog/posts.html', {'posts': posts})

# <<<<<<<<<<<< here
def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_create(request):
    if request.method == "POST":
        form = PostCreateForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_at = timezone.now()
            post.save()
            return redirect('post_detail', id=post.id)
    else:
        form = PostCreateForm()
    return render(request, 'blog/post_create.html', {'form': form})

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JWTAuthentication,))  # SimpleJWT 인증 클래스 사용
def posts_json(request):
    posts = Post.objects.filter(published_at__isnull=False).order_by('-published_at')
    post_list = serializers.serialize('json', posts)
    return HttpResponse(post_list, content_type="application/json")  # 적절한 Content-Type 설정