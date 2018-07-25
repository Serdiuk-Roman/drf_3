
from django.contrib.auth.models import User
from django.views.generic import ListView

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from post.models import Category, Post
from post.serializers import UserSerializer, CategorySerializer, PostSerializer
from post.permissions import IsOwnerOrReadOnly, IsStaffOrReadOnly


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class CategoryViewSet(viewsets.ModelViewSet):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsStaffOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostViewSet(viewsets.ModelViewSet):

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostIndex(ListView):
    template_name = "post/index.html"
    queryset = Post.objects.order_by('-created_on')
    context_object_name = 'post_list'
