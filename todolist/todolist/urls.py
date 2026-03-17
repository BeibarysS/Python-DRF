from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from tasks.views import ProjectViewSet, TaskViewSet, CommentViewSet

router = DefaultRouter()
router.register('projects', ProjectViewSet, basename='project')
router.register('tasks', TaskViewSet, basename='task')
router.register('tasks/(?P<task_pk>[^/.]+)/comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/auth/login/', TokenObtainPairView.as_view()),
    path('api/auth/refresh/', TokenRefreshView.as_view()),
    path('api/auth/', include('accounts.urls')),
]