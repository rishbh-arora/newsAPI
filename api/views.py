from rest_framework import permissions, authentication, viewsets, status
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

from .serializers import *
from .models import News, CustomUser
from .filters import NewsArticleFilter

from django.contrib.auth.hashers import make_password
from django_filters.rest_framework import DjangoFilterBackend

class NewsViewset(viewsets.ReadOnlyModelViewSet):
    queryset = News.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    serializer_class = NewsSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = NewsArticleFilter

class BookmarkViewset(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        data = {"article": pk, "user": request.user.id}
        serializer = BookmarkSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        try:
            user = Bookmarks.objects.get(pk=pk)
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CustomUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class RegisterView(CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')

        try:
            user = CustomUser.objects.get(username=username)
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

        except:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

class UserViewset(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    

    def put(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data)

        if 'karma' in request.data:
            return Response({"error': 'You cannot award or discard your karma points"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            if request.data.username != request.user.username:
                user = CustomUser.objects.get(username=request.data.username)
                return Response({"error': 'Username already in use"}, status=status.HTTP_400_BAD_REQUEST)
        
        except:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentsViewset(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]
    lookup_field = "user"


    @action(detail=False, methods=['get'])
    def by_article(self, request):
        article_id = request.query_params.get('article_id')
        queryset = self.get_queryset().filter(article_id=article_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_user(self, request):
        user = request.user
        queryset = self.get_queryset().filter(user=user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def perform_create(self, serializer):
        validated_data = serializer.validated_data
        user = self.request.user
        validated_data["user"] = user
        user.karma += 10
        user.save()
        serializer.save()

#14cd16c8cf1f3f7e6b0eb7115f8d83b7f1fd8fe2