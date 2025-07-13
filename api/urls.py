from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, RegisterView

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')
urlpatterns = router.urls

urlpatterns += [
    path('auth/register/', RegisterView.as_view(), name='auth_register'),
]
