import os

from PIL import Image
from rest_framework import (generics, permissions, response, status, views,
                            viewsets)
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.views import APIView
from rest_framework_simplejwt import views

from api.models import *
from api.serializers import *


class NoticeViewSet(viewsets.ModelViewSet):
    queryset = Notice.objects.all().order_by('creation_date')
    serializer_class = NoticeSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            instance = serializer.save(creator=self.request.user)
            
        else:
            instance = serializer.save()
        


class RegisterViewSet(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer


class MyTokenObtainPairView(views.TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class GetUserViewSet(generics.ListAPIView):
    def get_queryset(self):
        queryset = User.objects.filter(id=self.kwargs['pk'])
        return queryset

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GetUserSerializer


class AllUserViewSet(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AllUserSerializer

    def get_queryset(self):
        queryset = User.objects.all()
        return queryset


class AllNoticeCreatedFromUser(generics.ListAPIView):
    serializer_class = NoticeCreatedFromUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Notice.objects.filter(creator_id=self.kwargs['pk'])
        return queryset


class NoticeCreatedFromUser(generics.ListAPIView):
    serializer_class = NoticeCreatedFromUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Notice.objects.filter(
            creator_id=self.kwargs['pk'], id=self.kwargs['id'])
        return queryset

    def delete(self, request, *args, **kwargs):
        queryset = Notice.objects.get(
            creator_id=self.kwargs['pk'], id=self.kwargs['id'])
        path = str(queryset.image_url.path)
        print(path)
        if os.path.exists(path):
            print('True')
            os.remove(path)
            queryset.delete()
            return response.Response(status=status.HTTP_200_OK)
        else:
            return response.Response(status=status.HTTP_404_NOT_FOUND)
class FileNoticeCreatedFromUser(generics.ListAPIView):

    serializer_class = FileNoticeCreatedFromUserSerializer
    permission_classes = [permissions.IsAuthenticated]
    # authentication_classes = [SessionAuthentication, BasicAuthentication]

    def get(self, request, *args, **kwargs):
        queryset = Notice.objects.filter(
            creator_id=self.kwargs['pk'], id=self.kwargs['id'])
        path = str(queryset.get().image_url.path)
        print(path)

        if os.path.exists(path):
            file = Image.open(path, 'r')

            file.show()
            return response.Response(status=status.HTTP_200_OK)

        else:
            return response.Response(status=status.HTTP_404_NOT_FOUND)


class NoticeUploadViewSet(APIView):
    parser_classes = [MultiPartParser,FormParser]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request,*args, **kwargs):
        images = Notice.objects.filter(creator_id=self.kwargs['pk'])
        for image in images:
            if image.title.lower() == str(request.data['title']).lower():
                return response.Response("Duplicate name", status=status.HTTP_409_CONFLICT)
        if str(request.data['image']).split('.')[1] != 'png' and str(request.data['image']).split('.')[1] != 'jpg':
            return response.Response("Invalid file extension. Only .jpg and .png files.", status=status.HTTP_400_BAD_REQUEST)



        image_url = request.FILES['image']

        serializer = ImagesSerializer(data=request.data,context={'image':image_url})

        
        if serializer.is_valid():
            if request.data.get('image') is not None:
                image_url.name = request.data.get('image').name
                creator = self.kwargs['pk']
                serializer.save(image_url=image_url,creator_id=creator)
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)