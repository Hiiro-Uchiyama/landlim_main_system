# coding: utf-8

from rest_framework import serializers
from ..models import Post, Tag, Category, Comment

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('name', 'mail')

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('tag',)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('title', 'body', 'created_at', 'status', 'author')

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('title', 'body', 'created_at', 'status', 'author')
