from django.shortcuts import render, get_object_or_404, redirect
from django.core import serializers
from django.core.paginator import Paginator

from django.http import JsonResponse
from django.utils import timezone
from django.utils.timezone import now
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import Post
from .forms import SignUpForm, PostCreateForm, PostUpdateForm
from .serializers import PostSerializer, PostUpdateSerializer

# for local application only
def default_layout(request):
    # 전달할 컨텍스트 데이터 (필요한 경우)
    context = {
        "title": "Default Layout",
        "message": "Welcome to the Default Layout Page",
    }
    return render(request, "blog/home.html", context)

# for local application only
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # 사용자 인증
            user = authenticate(username=user.username, password=form.cleaned_data['password1'])

            if user is not None:
                login(request, user)
                return redirect('home')  # 홈 페이지로 리다이렉트
    else:
        form = SignUpForm()
    return render(request, 'blog/signup.html', {'form': form})

# for local application only
def about(request):
    return render(request, 'blog/about.html')  # about.html 템플릿을 렌더링

@login_required
def posts(request):
    # 로그인한 사용자에 의해 작성된 게시물 필터링 및 정렬
    posts = Post.objects.filter(author=request.user, published_at__isnull=False).order_by('-published_at')
    # 페이지네이션 처리
    paginator = Paginator(posts, 3)  # 한 페이지에 3개의 게시물 표시
    page_number = request.GET.get('page')  # 쿼리 매개변수로 페이지 번호 가져오기
    page_obj = paginator.get_page(page_number)
    # 렌더링
    return render(request, 'blog/posts.html', {'page_obj': page_obj})


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


def post_update(request, id):
    post = get_object_or_404(Post, id=id)

    if request.method == "POST":
        form = PostUpdateForm(request.POST, instance=post)  # 기존 데이터를 폼에 바인딩
        if form.is_valid():
            form.save()  # 폼 데이터 저장
            return redirect('post_detail', id=post.id)  # 저장 후 상세 페이지로 이동
    else:
        form = PostUpdateForm(instance=post)  # GET 요청 시 기존 데이터로 폼 초기화

    return render(request, 'blog/post_update.html', {'form': form, 'post': post})


def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    return redirect('posts')


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JWTAuthentication,))  # SimpleJWT 인증 클래스 사용
def posts_json(request):
    posts = Post.objects.filter(published_at__isnull=False).order_by('-published_at')
    post_list = serializers.serialize('json', posts)
    return JsonResponse(post_list, safe=False, content_type="application/json")


# for frontend only
@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JWTAuthentication, ))
def posts_api(request):
    if request.method == 'GET':
        posts = Post.objects.filter(published_at__isnull=False).order_by('-published_at')

        # Pagination 처리
        page_size = 3  # 한 페이지에 표시할 게시물 수
        paginator = Paginator(posts, page_size)
        page_number = request.GET.get('page', 1)  # 기본적으로 1페이지로 설정
        page_obj = paginator.get_page(page_number)

        # JSON 데이터 구성
        posts_data = [
            {
                'id': post.id,
                'title': post.title,
                'content': post.content,
                'created_at': post.created_at,
                'updated_at': post.updated_at,
                'published_at': post.published_at,
                'author': post.author.username,
            } for post in page_obj
        ]

        response_data = {
            'count': paginator.count,  # 총 게시물 수
            'total_pages': paginator.num_pages,  # 총 페이지 수
            'current': page_obj.number,  # 현재 페이지 번호
            'next': page_obj.next_page_number() if page_obj.has_next() else None,  # 다음 페이지 번호
            'previous': page_obj.previous_page_number() if page_obj.has_previous() else None,  # 이전 페이지 번호
            'results': posts_data,  # 현재 페이지의 게시물 데이터
        }

        return JsonResponse(response_data)

# for frontend only
@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JWTAuthentication, ))
def post_detail_api(request, id):
    # 게시물을 가져오거나 404 오류 반환
    post = get_object_or_404(Post, id=id)

    # 게시물 데이터를 JSON 형식으로 변환
    post_data = {
        'id': post.id,
        'title': post.title,
        'content': post.content,
        'created_at': post.created_at,
        'updated_at': post.updated_at,
        'published_at': post.published_at,
        'author': post.author.username,  # 작성자 이름 포함
    }

    # JSON 응답 반환
    return JsonResponse(post_data)


# for frontend only
@csrf_exempt  # Vue.js에서 CSRF 토큰 없이 요청할 경우 필요
@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JWTAuthentication, ))  # 튜플로 전달
def post_create_api(request):
    if request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            post = serializer.save(author=request.user, published_at=now())
            return Response({'id': post.id, 'message': 'Post created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt  # Vue.js에서 CSRF 토큰 없이 요청할 경우 필요
@api_view(['PUT', 'PATCH'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JWTAuthentication, ))
def post_update_api(request, id):
    post = get_object_or_404(Post, id=id)

    if request.method == 'PUT':
        serializer = PostUpdateSerializer(post, data=request.data, partial=False)  # 전체 업데이트
    elif request.method == 'PATCH':
        serializer = PostUpdateSerializer(post, data=request.data, partial=True)  # 부분 업데이트

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt  # Vue.js에서 CSRF 토큰 없이 요청할 경우 필요
@api_view(['DELETE'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((JWTAuthentication, ))
def post_delete_api(request, id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    return Response({"message": "Post deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
