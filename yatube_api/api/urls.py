from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import CommentViewSet, FollowViewSet, GroupViewSet, PostViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(
    r'posts/(?P<post_id>\d+)/comments',
    CommentViewSet, basename='comment'
)
router.register(r'groups', GroupViewSet, basename='group')
router.register(r'follow', FollowViewSet, basename='follow')

urlpatterns = [
    path('', include(router.urls)),
    path(
        'api/token/', TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'api/token/refresh/',
        TokenRefreshView.as_view(), name='token_refresh'
    ),
]
