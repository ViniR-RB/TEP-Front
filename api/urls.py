from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import *

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterViewSet.as_view(), name='auth_register'),
    path('users/', AllUserViewSet.as_view(), name="Users"),
    path('users/<int:pk>/notice/', AllNoticeCreatedFromUser.as_view(),
         name='all_notice_from_user'),
    path('users/<int:pk>/notice/<int:id>',
         NoticeCreatedFromUser.as_view(), name='notice_created_from_user'),
    path('users/<int:pk>/notice/<int:id>/file',
         FileNoticeCreatedFromUser.as_view(), name='notice_image_created_from_user'),
    path('users/<int:pk>/notice/file/', NoticeUploadViewSet.as_view(),
         name='notice_image_created_from_user_upload'),
    path('users/<int:pk>/', GetUserViewSet.as_view(), name='get_user_from_id'),
]
