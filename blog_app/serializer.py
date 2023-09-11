from rest_framework import serializers
from .models import Author, Blog
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')

class AuthorSerializer(serializers.ModelSerializer):
    user = UserSerializer(write_only=True)  

    class Meta:
        model = Author
        fields = ('id', 'user', 'bio')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        author = Author.objects.create(user=user, **validated_data)
        return author
    


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'
        
        
class AuthorWithBlogsSerializer(serializers.ModelSerializer):
    blogs = BlogSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ('id', 'user', 'bio', 'blogs')
        
class AuthorUpdateSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False) 

    class Meta:
        model = Author
        fields = ('bio', 'user')

    def update(self, instance, validated_data):
        # Update Author fields
        instance.bio = validated_data.get('bio', instance.bio)
        
        user_data = validated_data.get('user')
        if user_data:
            user = instance.user
            user.username = user_data.get('username', user.username)
            user.email = user_data.get('email', user.email)
            user.first_name = user_data.get('first_name', user.first_name)
            user.last_name = user_data.get('last_name', user.last_name)
            user.save()
        
        instance.save()
        return instance




        
