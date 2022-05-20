# coding: utf-8

from rest_framework import routers
from .view_set import PostViewSet, TagViewSet, CategoryViewSet, CommentViewSet

router = routers.DefaultRouter()
router.register(r'post_view', PostViewSet)
router.register(r'tag_view', TagViewSet)
router.register(r'category_view', CategoryViewSet)
router.register(r'comment_view', CommentViewSet)