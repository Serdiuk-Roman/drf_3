from django.contrib.auth.models import User
from rest_framework import serializers

from post.models import Category, Post


class UserSerializer(serializers.ModelSerializer):

    date_joined = serializers.ReadOnlyField()
    is_staff = serializers.ReadOnlyField()

    class Meta:
        model = User
        # fields = "__all__"
        fields = (
            'url',
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'is_staff',
            'is_active',
            'date_joined'
        )


class CategorySerializer(serializers.ModelSerializer):

    user = serializers.ReadOnlyField(source='user.username')
    link = serializers.HyperlinkedIdentityField(view_name='category-detail')

    class Meta:
        model = Category
        fields = ('link', 'name', 'description', 'is_active', 'user')


class PostSerializer(serializers.ModelSerializer):

    user = serializers.ReadOnlyField(source='user.username')
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='name')
    link = serializers.HyperlinkedIdentityField(view_name='post-detail')

    class Meta:
        model = Post
        fields = (
            'id',
            'link',
            'status',
            'category',
            'user',
            'title',
            'content',
            'created_on',
            'updated_on',
        )
