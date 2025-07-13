from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Project
from .serializers import ProjectSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from .permissions import IsOwnerOrReadOnly


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return self.request.user.projects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'], url_path='complete')
    def complete(self, request, pk=None):
        """
        Mark a project as complete.
        """
        project = self.get_object()
        project.metadata['status'] = 'completed'
        project.save()
        serializer = self.get_serializer(project)
        return Response(serializer.data)
