from rest_framework import generics, permissions,status
from .models import Author, Blog
from .serializer import AuthorSerializer, BlogSerializer, AuthorUpdateSerializer, AuthorWithBlogsSerializer
from rest_framework.response import Response
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import UpdateAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import PermissionDenied

class RegisterView(generics.CreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        author = serializer.save()
        return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
    

class LoginAuthor(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        
        
class AuthorListView(generics.ListAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorWithBlogsSerializer
    
class AuthorDetailView(generics.RetrieveAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorWithBlogsSerializer
    lookup_field = 'id' 

    def retrieve(self, request, *args, **kwargs):
        try:
            author = self.get_object()
            serializer = self.get_serializer(author)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Author.DoesNotExist:
            return Response({'detail': 'Author not found'}, status=status.HTTP_404_NOT_FOUND)
        
    
class AuthorUpdateView(generics.UpdateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorUpdateSerializer
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        try:
            author = self.get_object()
            serializer = self.get_serializer(author, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Author updated successfully'}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Author.DoesNotExist:
            return Response({'detail': 'Author not found'}, status=status.HTTP_404_NOT_FOUND)
    
class AuthorDeleteView(generics.DestroyAPIView):
    queryset = Author.objects.all()

    def delete(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        try:
            user = Author.objects.get(pk=user_id)
            user.delete()
            return Response({'detail': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
class CreateBlogView(generics.CreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        author, created = Author.objects.get_or_create(user=self.request.user)
        serializer.save(author=author)


class BlogListView(generics.ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    
class BlogDetailView(generics.RetrieveAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    lookup_url_kwarg = 'blog_id'
    
class BlogDeleteView(generics.DestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        if obj.author.user != self.request.user:
            raise PermissionDenied("You do not have permission to delete this blog post.")
        return obj

    def perform_destroy(self, instance):
        instance.delete()
        
class BlogUpdateView(generics.UpdateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        if obj.author.user != self.request.user:
            raise PermissionDenied("You do not have permission to update this blog post.")
        return obj