from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from api.views import *

router = routers.DefaultRouter()
router.register('notice', NoticeViewSet, basename='notices')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
] + router.urls
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
