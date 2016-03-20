from api.models import *
from api.serializers import *
from rest_framework import generics, permissions, pagination
from rest_framework.response import Response
from django.contrib.auth.models import User
from friendship.models import Friend
from django.db.models import Q
import uuid
import copy


class UserPostList(generics.ListAPIView):
    """
    posts that are visible to the currently authenticated user (GET)
    http://service/author/posts 
    """

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PostSerializer

    def get_queryset(self):
        """
        This view should return a list of all the posts
        that are visible to the currently authenticated user
        """
        # TODO add friend logic
        posts = Post.objects.filter(
            Q(visibility='PUBLIC') |
            Q(author=Author.objects.get(user=self.request.user)))
        return posts


class PostList(generics.ListCreateAPIView):
    """
    List all Public Posts on the server(GET)
    http://service/posts
    """
    queryset = Post.objects.filter(visibility='PUBLIC')
    serializer_class = PostSerializer
    permission_classes = (permissions.AllowAny,)

    def perform_create(self, serializer):
        serializer.save(author=Author.objects.get(user=self.request.user))


# TODO FINISH  all, doesnt work (get UUID working with User)
class AuthorPostList(generics.ListAPIView):
    """
    all posts made by {AUTHOR_ID} visible to the currently authenticated user (GET)
    http://service/author/{AUTHOR_ID}/posts 
    """
    serializer_class = PostSerializer
    permission_classes = (permissions.AllowAny,)
    lookup_url_kwarg = 'uuid'

    def get_queryset(self):
        requestId = self.kwargs.get(self.lookup_url_kwarg)
        user = User.objects.filter(Author__uuid=requestId)
        posts = Post.objects.filter(User__pk=user.pk)
        return uuid



class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    access to a single post with id = {POST_ID}
    http://service/posts/{POST_ID}
    """
    serializer_class = PostSerializer
    # TODO change to something more approp
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    lookup_url_kwarg = 'uuid'
    # add visibility logic
    def get_queryset(self):
        requestId = self.kwargs.get(self.lookup_url_kwarg)
        # TODO Should be a .get but w/e
        return Post.objects.filter(identity=uuid.UUID(requestId))

    def perform_create(self, serializer_class):
        author = Author.objects.filter(user=self.request.user)
        serializer_class.save(author=author)


    
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = AuthorSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = AuthorSerializer

class FriendRelationship(generics.ListCreateAPIView):
    """
    Returns your friend relationship with a certain author
    http://service/friends/(?P<uuid>[^/]+)
    """
    queryset = Author.objects.all()
    serializer_class = FriendSerializer

    lookup_url_kwarg = 'uuid'

    def get_queryset(self):
        # Get the uuid from the url
        request_id = self.kwargs.get(self.lookup_url_kwarg)
        # Find the author object with that uuid
        username = Author.objects.get(uuid=request_id)
        # Get all the friends
        all_friends = Friend.objects.friends(username.user)
        # Get the authors objects version of those friends objects
        all_authors = Author.objects.filter(user__in=all_friends)
        return all_authors


class FriendsCheck(generics.ListCreateAPIView):
    """
    Returns your friend relationship with a certain author
    http://service/friends/(?P<uuid>[^/]+)/(?P<uuid>[^/]+)
    """
    queryset = Author.objects.all()
    serializer_class = FriendsCheckSerializer()

    lookup_url_kwarg_1 = 'friend1_uuid'
    lookup_url_kwarg_2 = 'friend2_uuid'

    def get_queryset(self):
        # Get the uuid from the url
        request_id_1 = self.kwargs.get(self.lookup_url_kwarg_1)
        request_id_2 = self.kwargs.get(self.lookup_url_kwarg_2)
        # Find the author object with that uuid
        username_1 = Author.objects.get(uuid=request_id_1)
        username_2 = Author.objects.get(uuid=request_id_2)
        # Check if friends
        result = Friend.objects.are_friends(username_1.user, username_2.user)
        authors2 = list()
        authors2.append(request_id_1)
        authors2.append(request_id_2)
        friend_pair = FriendsPair(authors2, result)
        resultlist = list()
        resultlist.append(friend_pair)
        return resultlist

#####################
# from api.models import Post
# from api.post_serializers import PostSerializer
# from rest_framework import generics


# class PostList(generics.ListCreateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer


# class PostDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer


#=========================================================================
# these are equal lol

# from api.models import Post
# from api.post_serializers import PostSerializer
# from django.http import Http404
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status


# class PostList(APIView):
#     """
#     List all posts, or create a new post.
#     """
#     def get(self, request):
#         posts = Post.objects.all()
#         serializer = PostSerializer(posts, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = PostSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class PostDetail(APIView):
#     """
#     Retrieve, update or delete a post.
#     """
#     def get_object(self, pk):
#         try:
#             return Post.objects.get(pk=pk)
#         except Post.DoesNotExist:
#             raise Http404

#     def get(self, request, pk):
#         post = self.get_object(pk)
#         serializer = PostSerializer(post)
#         return Response(serializer.data)

#     def put(self, request, pk):
#         post = self.get_object(pk)
#         serializer = PostSerializer(post, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         post = self.get_object(pk)
#         post.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
