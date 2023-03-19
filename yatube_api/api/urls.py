from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GroupViewSet, PostViewSet, CommentViewSet
from rest_framework.authtoken import views


router = DefaultRouter()
router.register('posts', PostViewSet, basename='posts')
router.register('groups', GroupViewSet, basename='groups')
router.register(r'posts/(?P<post_id>[^/.]+)/comments',
                CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', views.obtain_auth_token),
]
