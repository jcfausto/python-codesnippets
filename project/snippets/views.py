from django.contrib.auth.models import User
from snippets.models import Snippet 
from snippets.serializers import SnippetSerializer
from snippets.serializers import UserSerializer
from rest_framework import generics
from rest_framework import permissions
from snippets.permissions import IsOwnerOrReadOnly
from rest_framework.decorators import api_view
from rest_framework import renderers
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(('GET',))
def api_root(request, format=None):
	return Response({
		'users': reverse('user-list', request=request, format=format), 
		'snippets': reverse('snippet-list', request=request, format=format)
	})


class SnippetList(generics.ListCreateAPIView):
	"""
	List all code snippets, or create a new snippet
	"""
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

	queryset = Snippet.objects.all()
	serializer_class = SnippetSerializer

	def pre_save(self, obj):
		obj.owner = self.request.user

class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
	"""
	Retrieve, update or delete a code snippet. 
	"""
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,
						  IsOwnerOrReadOnly,)

	queryset = Snippet.objects.all()
	serializer_class = SnippetSerializer

	def pre_save(self, obj):
		obj.owner = self.request.user

class SnippetHighlight(generics.GenericAPIView):
	queryset = Snippet.objects.all()
	renderer_class = (renderers.StaticHTMLRenderer,)

	def get(self, request, *args, **kwargs):
		snippet = self.get_object()
		return Response(snippet.highlighted)

class UserList(generics.ListAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer

