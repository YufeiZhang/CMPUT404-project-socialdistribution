from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import Post, Author


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('uuid', 'host', 'displayName', 'url', 'github')



class UserSerializer(serializers.ModelSerializer):
    #userinfo = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    author = AuthorSerializer(source='author')
    class Meta:
        model = User
        fields = ('author')


# class AuthorSerializer(serializers.ModelSerializer):
#     posts = serializers.PrimaryKeyRelatedField(
#         many=True, queryset=Post.objects.all())

#     class Meta:
#         model = User
#         fields = ('identity', 'username', 'posts')


        
        
class PostSerializer(serializers.ModelSerializer):
    # TODO change source to = some user serializer with ID, host,displayname
    # url and github (see api protocols)
    author = AuthorSerializer(read_only=True)
    # test = AlbumSerializer(source='author')
    
    class Meta:
        model = Post
        fields = (
            'title', 'source', 'origin', 'description',
            'contentType', 'content', 'author', 'categories',
            'published', 'identity', 'visibility', 
        )


















